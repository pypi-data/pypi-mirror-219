import os

import streamlit as st
import pandas as pd

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _custom_dataframe = components.declare_component(
        "custom_dataframe",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _custom_dataframe = components.declare_component("custom_dataframe", path=build_dir)


def custom_dataframe(data, key=None):
    data = data.to_dict(orient='list') 
    editable_cell = {
        "New Pricing":[1,3],
        }
    shape = {
        "no_rows": 5,
        "no_cols": 5,
        "width": "500px",
        "height": "600px"
    }
    return _custom_dataframe(data=data, key=key, editable_cells=editable_cell,  colorable_cells=None)



# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run custom_dataframe/__init__.py`
if not _RELEASE:
    raw_data = {
        "Category": ["CCF Regional Accrual", "CTM Local Accrual", "Flex", "Other", "DNNSI"],
        "Current": [1, 2, 0, 0, 0],
        "New Pricing": [0, 0, 0, 0, 0],
        "Change $": [0, 0, 0, 0, 0],
        "Change%": [0, 0, 0, 0, 0]
    }
    st.dataframe(raw_data)
    df = pd.DataFrame(raw_data, columns=["Category", "Current", "New Pricing", "Change $", "Change%"])
    col1, col2, col3 = st.columns(3)
    with col1:
        returned_df = custom_dataframe(df, key=1)
    # with col2:
    #     returned_df = custom_dataframe(df, key=2)
    # with col3:
    #     returned_df = custom_dataframe(df, key=3)
    print(returned_df)
    st.table(pd.DataFrame(returned_df))
