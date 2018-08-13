#
# (C) Rob W.W. Hooft, 2004
# (C) Daniel Herding, 2004
# (C) Wikipedian, 2004-2008
# (C) leogregianin, 2004-2008
# (C) Ben McIlwain (CydeWeys), 2006-2015
# (C) Anreas J Schwab, 2007
# (C) xqt, 2009-2018
# (C) Pywikibot team, 2008-2018
# (C) Sami Moustachir 2018
# Distributed under the terms of the MIT license.
#

import pywikibot
import os
import pickle
import re
import tqdm

from pywikibot.tools import open_archive
from pywikibot import config

from py2neo import Graph, Node, Relationship


class CategoryDatabase(object):

    """Temporary database saving pages and subcategories for each category.
    This prevents loading the category pages over and over again.
    """

    def __init__(self, rebuild=False, filename='category.dump.bz2'):
        """Initializer."""
        if not os.path.isabs(filename):
            filename = config.datafilepath(filename)
        self.filename = filename
        if rebuild:
            self.rebuild()

    @property
    def is_loaded(self):
        """Return whether the contents have been loaded."""
        return hasattr(self, 'catContentDB') and hasattr(self, 'superclassDB')

    def _load(self):
        if not self.is_loaded:
            try:
                if config.verbose_output:
                    pywikibot.output('Reading dump from %s'
                                     % config.shortpath(self.filename))
                with open_archive(self.filename, 'rb') as f:
                    databases = pickle.load(f)
                # keys are categories, values are 2-tuples with lists as
                # entries.
                self.catContentDB = databases['catContentDB']
                # like the above, but for supercategories
                self.superclassDB = databases['superclassDB']
                del databases
            except Exception:
                # If something goes wrong, just rebuild the database
                self.rebuild()

    def rebuild(self):
        """Rebuild the dabatase."""
        self.catContentDB = {}
        self.superclassDB = {}

    def getSubcats(self, supercat):
        """Return the list of subcategories for a given supercategory.
        Saves this list in a temporary database so that it won't be loaded from
        the server next time it's required.
        """
        self._load()
        # if we already know which subcategories exist here
        if supercat in self.catContentDB:
            return self.catContentDB[supercat][0]
        else:
            subcatset = set(supercat.subcategories())
            articleset = set(supercat.articles())
            # add to dictionary
            self.catContentDB[supercat] = (subcatset, articleset)
            return subcatset

    def getArticles(self, cat):
        """Return the list of pages for a given category.
        Saves this list in a temporary database so that it won't be loaded from
        the server next time it's required.
        """
        self._load()
        # if we already know which articles exist here
        if cat in self.catContentDB:
            return self.catContentDB[cat][1]
        else:
            subcatset = set(cat.subcategories())
            articleset = set(cat.articles())
            # add to dictionary
            self.catContentDB[cat] = (subcatset, articleset)
            return articleset

    def getSupercats(self, subcat):
        """Return the supercategory (or a set of) for a given subcategory."""
        self._load()
        # if we already know which subcategories exist here
        if subcat in self.superclassDB:
            return self.superclassDB[subcat]
        else:
            supercatset = set(subcat.categories())
            # add to dictionary
            self.superclassDB[subcat] = supercatset
            return supercatset

    def dump(self, filename=None):
        """Save the dictionaries to disk if not empty.
        Pickle the contents of the dictionaries superclassDB and catContentDB
        if at least one is not empty. If both are empty, removes the file from
        the disk.
        If the filename is None, it'll use the filename determined in __init__.
        """
        if filename is None:
            filename = self.filename
        elif not os.path.isabs(filename):
            filename = config.datafilepath(filename)
        if self.is_loaded and (self.catContentDB or self.superclassDB):
            pywikibot.output(u'Dumping to %s, please wait...'
                             % config.shortpath(filename))
            databases = {
                'catContentDB': self.catContentDB,
                'superclassDB': self.superclassDB
            }
            # store dump to disk in binary format
            with open_archive(filename, 'wb') as f:
                try:
                    pickle.dump(databases, f, protocol=config.pickle_protocol)
                except pickle.PicklingError as e:
                    pywikibot.output(e)
        else:
            try:
                os.remove(filename)
            except EnvironmentError as e:
                pywikibot.output(e)
            else:
                pywikibot.output(u'Database is empty. %s removed'
                                 % config.shortpath(filename))

    def dump_neo(self, host, user, password):
        self._load()

        graph = Graph(host=host, user=user, password=password)
        graph.schema.create_uniqueness_constraint('Categorie', 'name')
        graph.schema.create_uniqueness_constraint('Article', 'name')
        graph.schema.create_index('Categorie', 'name')
        graph.schema.create_index('Article', 'name')

        pattern = r'Category:(.*)'
        categories = {}

        # building nodes
        for cat, t in tqdm.tqdm(self.catContentDB.items()):
            if cat.pageid not in categories:
                categories[cat.pageid] = Node('Categorie',
                    name=re.search(pattern, cat.title()).group(1),
                    url=cat.full_url(),
                    depth=cat.depth
                )
            subcats = t[0]
            art = t[1]
            for subcat in subcats:
                if subcat.pageid not in categories:
                    n = Node('Categorie',
                             name=re.search(pattern, subcat.title()).group(1),
                             url=subcat.full_url(),
                             depth=subcat.depth
                             )
                    categories[subcat.pageid] = n
                    graph.create(n)
                    graph.create(Relationship(categories[cat.pageid],
                                 'HAS_SUBCLASS', n))
            for a in art:
                n = Node('Article',
                         name=a.title(),
                         url=a.full_url())
                graph.create(n)
                graph.create(Relationship(categories[cat.pageid],
                             'HAS_ARTICLE', n))


class CategoryTreeRobot(object):

    """Robot to create tree overviews of the category structure.
    Parameters:
        * catTitle - The category which will be the tree's root.
        * catDB    - A CategoryDatabase object
        * maxDepth - The limit beyond which no subcategories will be listed.
                     This also guarantees that loops in the category structure
                     won't be a problem.
        * filename - The textfile where the tree should be saved; None to print
                     the tree to stdout.
    """

    def __init__(self, catTitle, catDB, filename=None, maxDepth=10, lang='en', source='wikipedia'):
        """Initializer."""
        self.catTitle = catTitle
        self.catDB = catDB
        if filename and not os.path.isabs(filename):
            filename = config.datafilepath(filename)
        self.filename = filename
        self.maxDepth = maxDepth
        self.site = pywikibot.Site(lang, source)

    def treeview(self, cat, currentDepth=0, parent=None):
        """Return a tree view of all subcategories of cat.
        The multi-line string contains a tree view of all subcategories of cat,
        up to level maxDepth. Recursively calls itself.
        Parameters:
            * cat - the Category of the node we're currently opening
            * currentDepth - the current level in the tree (for recursion)
            * parent - the Category of the category we're coming from
        """
        result = u'#' * currentDepth
        if currentDepth > 0:
            result += u' '
        result += ' (%d)' % cat.categoryinfo['pages']
        if currentDepth < self.maxDepth // 2:
            # noisy dots
            pywikibot.output('.', newline=False)
        # Create a list of other cats which are supercats of the current cat
        supercat_names = [re.search('Category:(.*)', super_cat.title()).group(1)
                          for super_cat in self.catDB.getSupercats(cat)
                          if super_cat != parent]
        if supercat_names:
            # print this list, separated with commas, using translations
            # given in 'category-also-in'
            comma = self.site.mediawiki_message('comma-separator')
            result += ' ' + comma.join(supercat_names)
        del supercat_names
        result += '\n'
        if currentDepth < self.maxDepth:
            for subcat in self.catDB.getSubcats(cat):
                # recurse into subdirectories
                result += self.treeview(subcat, currentDepth + 1, parent=cat)
        elif self.catDB.getSubcats(cat):
            # show that there are more categories beyond the depth limit
            result += '#' * (currentDepth + 1) + ' [...]\n'
        return result

    def parse(self, cat, currentDepth=0):
        """
        Parse each stage while giving information about the progress.
        Parameters:
            * cat - the Category of the node we're currently opening
            * currentDepth - the current level in the tree
        """
        while currentDepth < self.maxDepth:
            pywikibot.output('Reading depth : %s/%s' 
                            %(currentDepth, self.maxDepth - 1))
            if currentDepth == 0:
                init_set = {cat}
            control_set = set()
            for cat in tqdm.tqdm(init_set):
                supernames = self.catDB.getSupercats(cat)
                articles = self.catDB.getArticles(cat)
                control_set = control_set.union(self.catDB.getSubcats(cat))
            init_set = control_set
            currentDepth += 1

    def run(self):
        """Handle the multi-line string generated by treeview.
        After string was generated by treeview it is either printed to the
        console or saved it to a file.
        """
        cat = pywikibot.Category(self.site, self.catTitle)
        tree = self.parse(cat)


if __name__ == '__main__':
    catDB = CategoryDatabase(rebuild=True)
    bot = CategoryTreeRobot('Scientific_disciplines', catDB, maxDepth=6)
    bot.run()
    catDB.dump_neo(host='localhost', user='neo4j', password='admin')
