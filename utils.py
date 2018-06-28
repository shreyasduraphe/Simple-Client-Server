class Parse(object):

    @staticmethod
    def extract(filename):
        try:
            data_list = filename.split('\\r\\n')
            return data_list[0].split(' ')[1].lstrip('/')
        except Exception as e:
            pass
        return ''