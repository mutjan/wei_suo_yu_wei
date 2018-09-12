class Idiom():
    def __init__(self,file='idioms_.txt'):
        self.data = self.load_idioms(file)
        #key为所有成语的第四字，value为所有能接上key的成语的第四字
        self.forward_paths = self.parse_path(self.data)
        # key为所有成语的第一字，value为所有能被key接上的成语的第一字
        self.backward_paths = self.parse_path(self.data, True)

    def load_idioms(self,file,encoding='utf-8'):
        idioms = []
        with open(file,'r',encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip()
                splited = line.split(' ')
                idioms.append(splited[0])
        return idioms

    def parse_path(self,idioms,reverse=False):
        result = {}
        for idiom in idioms:
            if reverse:
                idiom = idiom[::-1]
            if idiom[0] in result:
                if idiom[-1] not in result[idiom[0]]:
                    result[idiom[0]].append(idiom[-1])
            else:
                result[idiom[0]] = [idiom[-1]]
        return result

    def get_all_available(self,words,reverse=False):
        result = []

        if reverse:
            path = self.backward_paths
        else:
            path = self.forward_paths

        for word in list(words):
            if word in path:
                result.extend(path[word])

        return set(result)

    def find_path(self,start,end):
        if start[-1] == end[0]:
            return [start,end]

        path = [set([start[-1]])]
        path_to_end = self.get_all_available(end[0],reverse=True)
        flag = True

        while flag:
            next_level = self.get_all_available(path[-1])
            if next_level == set():
                return None
            path.append(next_level)
            for x in path[-1]:
                # 保证路径最短
                if x in path_to_end:
                    flag = False

        path[-1] = path[-1] & path_to_end
        path.append(end[0])
        path = path[::-1]

        # 从可行路径中随机选一条结果
        result = [end]

        for i in self.data:
            if i[-1] in list(path[0]) and (i[0] in list(path[1])):
                result.append(i)
                break
        for n in range(len(path) - 2):
            n = n + 1
            flag = True
            while flag:
                for i in self.data:
                    if i[-1] == result[-1][0] and (i[0] in list(path[n + 1])):
                        result.append(i)
                        break
                flag = False
        result.append(start)
        return result[::-1]

if __name__ == '__main__':
    idioms = Idiom()
    while True:
        start = input('start:').strip()
        end =  input('end(默认\'为所欲为\'):').strip() or '为所欲为'

        print('->'.join(idioms.find_path(start,end)))