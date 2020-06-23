from .table_reader import table_reader

class FormulaManager:

    def __init__(self, name):
        reader = table_reader
        data   = reader.fetch_row(name)

        formula_data_gen = {
            'T': 0.0166666666666667, # 1/60 = 1 minute expressed in fraction of an hour
            'Pme': data['Pme'],
            'Pae': data['Pae']
        }

        formula_data_man = {
            'LFme': 0.25,
            'LFae': 0.8,
            'EFme': 0.67,
            'EFae': 0.67
        }

        formula_data_ab = {
            'LFme': 0.25,
            'LFae': 0.7,
            'EFme': 0.18,
            'EFae': 0.18
        }

        self.emissions_man = self.__dragovic_et_al_formula(
            *formula_data_gen.values(),
            *formula_data_man.values()
        )

        self.emissions_ab  = self.__dragovic_et_al_formula(
            *formula_data_gen.values(),
            *formula_data_ab.values()
        )
    
    def __dragovic_et_al_formula(self, T, Pme, Pae, LFme, LFae, EFme, EFae):
        # Emissions from main engine
        me = Pme * LFme * EFme
        # Emissions from auxilary engine
        ae = Pae * LFae * EFae

        # Emissions in tons
        emissions = T * (me + ae)

        return emissions * 1000000
    
    def get_manouvering(self):
        '''
        Returns PM emissions for the manouvering state for `ship_name` per minute
        '''
        return self.emissions_man

    def get_idle(self):
        '''
        Returns PM emissions for the idle state for `ship_name` per minute
        '''
        return self.emissions_ab