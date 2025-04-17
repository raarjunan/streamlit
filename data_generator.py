import pandas as pd
import numpy as np
import networkx as nx
from wordcloud import WordCloud
from datetime import datetime, timedelta

def generate_general_dataset(n=365):
    import numpy as np
    import pandas as pd

    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=n, freq='D')
    
    data = pd.DataFrame({
        'date': dates,
        'sales': np.random.poisson(200, n) + np.linspace(0, 300, n),
        'revenue': np.random.normal(5000, 1000, n).round(2),
        'cost': np.random.normal(3500, 800, n).round(2),
        'customer_count': np.random.randint(50, 300, n),
        'conversion_rate': np.clip(np.random.normal(0.08, 0.03, n), 0, 0.2),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n),
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], n),
        'status': np.random.choice(['Open', 'In Progress', 'Complete', 'On Hold'], n),
        'channel': np.random.choice(['Online', 'Retail', 'Wholesale'], size=n),
        'lat': np.random.uniform(37.0, 38.0, size=n),
        'lon': np.random.uniform(-123.0, -122.0, size=n),
        'conversion_rate': np.clip(np.random.normal(0.08, 0.03, n), 0, 0.2),
    })

    # Injecting anomalies
    data.loc[np.random.choice(n, 5), 'sales'] *= 3
    data.loc[np.random.choice(n, 5), 'revenue'] *= -1

    # 🔧 Add parent_category
    data['parent_category'] = data['product_category'].map({
        'Electronics': 'Goods',
        'Clothing': 'Apparel',
        'Home': 'Goods',
        'Books': 'Media'
    })

    return data

def generate_network_data():
    G = nx.random_geometric_graph(15, 0.4)
    return G

def generate_bipartite_data():
    B = nx.Graph()
    B.add_nodes_from(['A1', 'A2', 'A3'], bipartite=0)
    B.add_nodes_from(['B1', 'B2'], bipartite=1)
    B.add_edges_from([('A1', 'B1'), ('A2', 'B2'), ('A3', 'B1')])
    return B

def generate_text_data():
    return ' '.join(np.random.choice(['electronics', 'books', 'tech', 'support', 'fashion'], 500))

def generate_kpi_spike_data():
    dates = pd.date_range("2024-01-01", periods=60)
    values = np.random.normal(5, 2, 60)
    values[15] = 20  # Spike
    values[35] = -5  # Dip
    return pd.DataFrame({'date': dates, 'value': values})
