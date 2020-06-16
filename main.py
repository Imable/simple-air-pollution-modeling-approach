from pre.init import Init
from process.model import Model
from post.analyse import Analyse

if __name__ == "__main__":
    conf = Init().get_conf()

    res  = Model(
        conf['start_ts'],
        conf['end_ts'],
        conf['step'],
        conf['source_data'],
        conf['debug']).run()

    Analyse(res)


    