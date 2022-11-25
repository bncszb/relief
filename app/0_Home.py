import streamlit as st

if __name__ == '__main__':
    st.set_page_config(
        layout="wide",
    )

    st.title("relief")
    st.markdown("""
    ## Funkciók
    ### 1. News
    A megyei hírportálok egy napnál nem régebbi, egy megadott kulcsszót tartalmazó híreit gyűjti össze táblázatosan.
    ### 2. Rain
    Villámárvíz felfedezését segíti, az OMSZ radar adatai és a domborzatból számított vízgyűjtőterületek alapján.
    ### 3. Shelter
    Egy adott kárhelyszín közelében lévő települések és az ott működöő közoktatási intézmények vezetőinek elérhetőségeit gyűjti össze.
    """)