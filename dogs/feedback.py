import streamlit as st

st.set_page_config(page_title="Feedback Form", page_icon="📄")
st.title("Feedback Form")
st.subheader("Give Us Feedback !")

def generate_feedback(first_name, last_name, rating, message):
    feedback = f"Thank you, {first_name} {last_name}! For your feedback! \nRating:{rating} \nMessage: {message}"
    return feedback

def main():
    col1, col2 = st.columns([2, 2])
    
    with col1:
        first_name = st.text_input("Enter your First name:")
    with col2:
        last_name = st.text_input("Enter your Last name:")

    rating = st.selectbox("Rate your experience ⭐", options=[1, 2, 3, 4, 5])
    message = st.text_area("Feedback Message:")

    if st.button("Submit Feedback"):
        if first_name and last_name and message:
            feedback = generate_feedback(first_name, last_name, rating, message)
            st.success(feedback)
        else:
            st.error("Please fill all the required fields!")

if __name__ == "__main__":
    main()
