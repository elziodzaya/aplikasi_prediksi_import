import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def build_fuzzy_system():
    market_demand = ctrl.Antecedent(np.arange(200, 401, 1), 'market_demand')
    product_stock = ctrl.Antecedent(np.arange(100, 251, 1), 'product_stock')
    production_capacity = ctrl.Antecedent(np.arange(0, 211, 1), 'production_capacity')
    product_import = ctrl.Consequent(np.arange(30, 401, 1), 'product_import')

    # Membership Functions
    market_demand['Low'] = fuzz.trimf(market_demand.universe, [200, 200, 300])
    market_demand['Medium'] = fuzz.trimf(market_demand.universe, [200, 300, 400])
    market_demand['High'] = fuzz.trimf(market_demand.universe, [300, 400, 400])

    product_stock['small'] = fuzz.trapmf(product_stock.universe, [75, 100, 130, 175])
    product_stock['Moderate'] = fuzz.trimf(product_stock.universe, [130, 175, 220])
    product_stock['Many'] = fuzz.trapmf(product_stock.universe, [175, 220, 250, 300])

    production_capacity['Low'] = fuzz.trapmf(production_capacity.universe, [0, 0, 60, 100])
    production_capacity['Medium'] = fuzz.trapmf(production_capacity.universe, [60, 100, 130, 170])
    production_capacity['High'] = fuzz.trapmf(production_capacity.universe, [130, 170, 210, 210])

    product_import['Low'] = fuzz.trapmf(product_import.universe, [30, 30, 90, 200])
    product_import['Medium'] = fuzz.trapmf(product_import.universe, [90, 200, 250, 350])
    product_import['High'] = fuzz.trapmf(product_import.universe, [250, 350, 400, 400])

    # Rule base (27 rules)
    rule_map = [
        ('Low','Many','High','Low'), ('Low','Many','Medium','Low'), ('Low','Many','Low','Low'),
        ('Low','Moderate','High','Low'), ('Low','Moderate','Medium','Low'), ('Low','Moderate','Low','Medium'),
        ('Low','small','High','Low'), ('Low','small','Medium','Medium'), ('Low','small','Low','Medium'),
        ('Medium','Many','High','Low'), ('Medium','Many','Medium','Medium'), ('Medium','Many','Low','Medium'),
        ('Medium','Moderate','High','Medium'), ('Medium','Moderate','Medium','Medium'), ('Medium','Moderate','Low','High'),
        ('Medium','small','High','Medium'), ('Medium','small','Medium','Medium'), ('Medium','small','Low','High'),
        ('High','Many','High','Medium'), ('High','Many','Medium','Medium'), ('High','Many','Low','High'),
        ('High','Moderate','High','Medium'), ('High','Moderate','Medium','Medium'), ('High','Moderate','Low','High'),
        ('High','small','High','Medium'), ('High','small','Medium','High'), ('High','small','Low','High')
    ]

    rules = [
        ctrl.Rule(market_demand[md] & product_stock[ps] & production_capacity[pc],
                  product_import[pi])
        for md, ps, pc, pi in rule_map
    ]

    system = ctrl.ControlSystem(rules)
    return system, market_demand, product_stock, production_capacity, product_import


def predict_import(system, md, ps, pc):
    sim = ctrl.ControlSystemSimulation(system)
    sim.input['market_demand'] = md
    sim.input['product_stock'] = ps
    sim.input['production_capacity'] = pc
    sim.compute()
    return sim.output['product_import']
