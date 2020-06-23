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
        conf['inversion_layer'],
        conf['pm_type'],
        conf['debug']).run()

    Analyse(
        res,
        conf['start_ts'],
        conf['end_ts'],
        conf['step'],
        conf['measurements_data'],
        conf['pm_type'],
        conf['station']
    )
