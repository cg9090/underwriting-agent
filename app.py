import streamlit as st

from agents.workflow import UnderwritingAgent


st.set_page_config(
    page_title="Company Research Agent"
)


def main():

    st.title("Company Research Agent")

    agent = UnderwritingAgent()


    if "companies" not in st.session_state:
        st.session_state.companies = None


    if "report" not in st.session_state:
        st.session_state.report = None


    company_input = st.text_input(
        "Enter company name or company number"
    )


    # Step 1: Find companies
    if st.button("Find Company"):
        st.session_state.companies = None
        st.session_state.selected_company = None
        st.session_state.report = None
        
        matches = agent.find_companies(
            company_input
        )

        if len(matches) == 0:

            st.error(
                "No company found."
            )

        else:

            st.session_state.companies = matches



    # Step 2: Select company
    if st.session_state.companies:

        companies = st.session_state.companies


        if len(companies) > 1:

            selected = st.selectbox(
                "Select company",
                companies,
                format_func=lambda c:
                    f"{c.company_name} ({c.company_number})"
            )

        else:

            selected = companies[0]

        st.write("### Selected Company")

        st.write(
            f"**Name:** {selected.company_name}"
        )

        st.write(
            f"**Company Number:** {selected.company_number}"
        )

        if st.button("Generate Report"):

            company = agent.company_house.get_company(
                selected.company_number
            )


            if company is None:

                st.error(
                    "Could not retrieve company."
                )

            else:

                with st.spinner(
                    "Researching..."
                ):

                    report = agent.investigate(
                        company
                    )


                st.session_state.report = report



    # Step 3: Display markdown report
    if st.session_state.report:

        st.divider()

        st.markdown(
            st.session_state.report
        )


if __name__ == "__main__":
    main()