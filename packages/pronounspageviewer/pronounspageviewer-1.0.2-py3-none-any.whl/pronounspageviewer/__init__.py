class Profile:
    base_opinions = {
        'yes': 'Yes',
        'no': 'Nope',
        'meh': 'Okay',
        'jokingly': 'Jokingly',
        'close': 'Only if we\'re close',
    }

    def __init__(self, profile_data: dict):
        self.data = profile_data
        self.opinions = dict(self.base_opinions)
        for opinion in self.data.get('opinions', {}):
            self.opinions[opinion] = self.data['opinions'][opinion].get(
                'description')

    def _print_opinion_list(self, heading: str, items: list, indent: str = ''):
        print(indent + heading)
        for item in items:
            print(indent, item.get('value'), self.opinions.get(
                item.get('opinion')), sep='\t')

    def _print_list(self, heading: str, key: str):
        print(heading + ':', ', '.join(self.data.get(key, [])))

    def _print_words(self):
        print('Words')
        for category in self.data.get('words', []):
            self._print_opinion_list(category.get(
                'header'), category.get('values', []), '\t')

    def _print_custom_flags(self):
        flags = self.data.get('customFlags', [])
        if len(flags) == 0:
            return
        print('Custom flags')
        for flag in flags:
            if flag.get('description'):
                print(f"\t{flag['name']}\t{flag['description']}")
            else:
                print('\t' + flag['name'])

    def print(self):
        if 'description' in self.data:
            print(self.data['description'])
        if 'age' in self.data:
            print('Age:', self.data['age'])
        if 'links' in self.data:
            self._print_list('Links', 'links')
        if 'flags' in self.data:
            self._print_list('Flags', 'flags')
        if 'customFlags' in self.data:
            self._print_custom_flags()
        print()
        if 'names' in self.data:
            self._print_opinion_list('Names', self.data['names'])
        if 'pronouns' in self.data:
            self._print_opinion_list('Pronouns', self.data['pronouns'])
        if 'words' in self.data:
            self._print_words()


def print_page(page: dict):
    print('Username:', page.get('username', '<no username>'))
    for profile in page.get('profiles', {}):
        print('Profile', profile)
        Profile(page['profiles'].get(profile, {})).print()
