from pre.init import Init
from process.run import Run
from post.analyse import Analyse

if __name__ == "__main__":
    conf = Init().get_conf()
    Run(
        conf['start_ts'],
        conf['end_ts'],
        conf['step'],
        conf['source_data'])
    Analyse()


    