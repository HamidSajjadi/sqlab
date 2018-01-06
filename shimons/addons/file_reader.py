import json


def read_patterns(path):
    patterns = list()
    with open(path) as reader:
        file = json.load(reader)
        for group in file['groupsInfo']:
            patterns.append(Pattern(group))
        return patterns


class Pattern:
    def __init__(self, group_info):
        self.name = group_info['groupName']
        self.inst_list = list()
        for i in group_info['instances']:
            self.inst_list.append(Instance(i))

    def __str__(self):
        return '{} : [{}]'.format(self.name, ', '.join(str(i) for i in self.inst_list))


class Instance:
    def __init__(self, instance):
        self.roles = set()
        for r in instance['entriesInfo']:
            self.roles.add(Role(r))

    def __str__(self):
        return 'Roles:<{}>'.format(', '.join(str(r) for r in self.roles))

    def __eq__(self, other):
        return self.roles == other.roles


class Role:
    def __init__(self, instance):
        self.class_id = instance['classId']
        self.role = instance['role']

    def __str__(self):
        return '{}:{}'.format(self.role, self.class_id)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash('{}{}'.format(self.role, self.class_id))
