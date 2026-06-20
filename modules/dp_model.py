import numpy as np
import pandas as pd

def dp_deterministic_horizon(
    demand,
    fuzzy_import,
    holding_cost,
    import_cost,
    max_stock,
    initial_stock
):
    """
    Deterministic finite-horizon Dynamic Programming
    Horizon: len(demand)
    """

    T = len(demand)

    # Action space dibatasi oleh fuzzy output
    def action_space(fuzzy_value):
        base = int(round(fuzzy_value))
        return sorted(set([
            max(0, base - 50),
            base,
            base + 50
        ]))

    V = np.zeros((T + 1, max_stock + 1))
    policy = np.zeros((T, max_stock + 1))

    # ===============================
    # BACKWARD DP
    # ===============================
    for t in reversed(range(T)):
        for s in range(max_stock + 1):
            best_cost = np.inf
            best_action = 0

            for a in action_space(fuzzy_import[t]):
                new_stock = s + a - demand[t]

                if new_stock < 0:
                    continue

                new_stock = min(max_stock, new_stock)

                cost = (
                    import_cost * a +
                    holding_cost * new_stock
                )

                total_cost = cost + V[t + 1, new_stock]

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_action = a

            V[t, s] = best_cost
            policy[t, s] = best_action

    # ===============================
    # FORWARD SIMULATION
    # ===============================
    stock = initial_stock
    results = []

    for t in range(T):
        action = int(policy[t, stock])
        new_stock = min(max_stock, stock + action - demand[t])

        holding_c = holding_cost * new_stock
        import_c = import_cost * action
        total_c = holding_c + import_c

        results.append({
            "Month": t + 1,
            "Demand": demand[t],
            "Impor_Fuzzy": round(float(fuzzy_import[t]), 2),
            "Impor_Optimal": action,
            "Stok_Awal": stock,
            "Stok_Akhir": new_stock,
            "Holding_Cost": holding_c,
            "Import_Cost": import_c,
            "Total_Cost": total_c
        })

        stock = new_stock

    df_result = pd.DataFrame(results)

    return df_result, V[0, initial_stock]
