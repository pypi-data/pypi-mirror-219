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


def custom_dataframe(data, key=None,editable_cell=None,shape=None,colorable_cells=None,colorable_text=None):
    data = data.to_dict(orient='list') 
    return _custom_dataframe(data=data, key=key, editable_cells=editable_cell,  colorable_cells=colorable_cells, shape=shape, colorable_text=colorable_text)



# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run custom_dataframe/__init__.py`
if not _RELEASE:
    raw_data = {
        "Category": ["CCF Regional Accrual", "CTM Local Accrual", "Flex", "Other", "DNNSI", ""],
        "Current": [1, 2, 0, 0, 0, ""],
        "New Pricing": [0, 0, 0, 0, 0, ""],
        "Change $": [0, 0, 0, 0, 0, ""],
        "Change%": [0, 0, 0, 0, 0, ""]
    }
    st.dataframe(raw_data)
    df = pd.DataFrame(raw_data, columns=["Category", "Current", "New Pricing", "Change $", "Change%"])
    editable_cell = {
        # "New Pricing":[1,3],
        }
    shape = {
        "no_rows": 6,
        "no_cols": 5,
        "width": "450px",
        "height": "200px"
    }
    colorable_cells  = {
    # "Category": ["yellow", "yellow", "", "", ""],
    # "Current": ["", "", "", "", ""],
    # "New Pricing": ["", "red", "", "red", ""],
    # "Change $": ["", "", "", "", ""],
    # "Change%": ["", "", "", "", ""]
    }
    colorable_text = {
    # "Category": ["yellow", "yellow", "", "", ""],
    # "Current": ["", "", "", "", ""],
    # "New Pricing": ["", "red", "", "red", ""],
    # "Change $": ["", "", "", "", ""],
    # "Change%": ["", "", "", "", ""]
    }
    merge_cell = {
        
    }
    custom_dataframe(df,key=1,editable_cell=editable_cell,shape= shape,colorable_cells=colorable_cells, colorable_text=colorable_text)
