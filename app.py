import streamlit as st
from PIL import Image
import os
import sqlite3

# Custom CSS to make the app look better
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Database setup
def init_db():
    conn = sqlite3.connect('dogs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dogs
                 (id INTEGER PRIMARY KEY, name TEXT, breed TEXT, address TEXT, age INTEGER, photo TEXT)''')
    conn.commit()
    conn.close()

def add_dog(name, breed, address, age, photo):
    if photo is not None:
        # Save photo in static/dog_photos directory
        img = Image.open(photo)
        os.makedirs("static/dog_photos", exist_ok=True)
        img_path = os.path.join("static", "dog_photos", f"{name}_{len(os.listdir('static/dog_photos'))}.png")
        img.save(img_path)
        
        conn = sqlite3.connect('dogs.db')
        c = conn.cursor()
        c.execute("INSERT INTO dogs (name, breed, address, age, photo) VALUES (?, ?, ?, ?, ?)",
                 (name, breed, address, age, img_path))
        conn.commit()
        conn.close()
        return True
    return False

def get_dogs(search="", page=1, per_page=6):
    conn = sqlite3.connect('dogs.db')
    c = conn.cursor()
    query = "SELECT * FROM dogs WHERE name LIKE ? OR breed LIKE ? OR address LIKE ?"
    c.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%"))
    all_dogs = c.fetchall()
    
    start = (page - 1) * per_page
    end = start + per_page
    dogs = all_dogs[start:end]
    
    conn.close()
    return dogs, len(all_dogs)

def adopt_dog(dog_id):
    conn = sqlite3.connect('dogs.db')
    c = conn.cursor()
    c.execute("SELECT photo FROM dogs WHERE id=?", (dog_id,))
    dog = c.fetchone()
    if dog and os.path.exists(dog[0]):
        os.remove(dog[0])
    
    c.execute("DELETE FROM dogs WHERE id=?", (dog_id,))
    conn.commit()
    conn.close()

def main():
    st.set_page_config(page_title="Paws & Purrs Adoption", layout="wide")
    local_css("style.css")
    
    # Initialize database
    init_db()
    
    # Header
    st.markdown("""
        <div class="header">
            <h1>🐾 Paws & Purrs Adoption 🐶</h1>
            <p>Find your new best friend today!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # About Us section
    st.markdown("""
        <div class="about-us">
            <h2>About Us</h2>
            <p>At Paws & Purrs, we believe every dog deserves a loving home. 
            Our mission is to connect adorable, adoptable dogs with their perfect 
            forever families. Browse our furry friends below and find your new companion!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for adding new dogs
    with st.sidebar:
        st.markdown('<h2 class="sidebar-header">Add a New Dog</h2>', unsafe_allow_html=True)
        name = st.text_input("Dog's Name")
        breed = st.text_input("Dog's Breed")
        address = st.text_input("Dog's Location")
        age = st.number_input("Dog's Age (in years)", min_value=0, max_value=20, step=1)
        photo = st.file_uploader("Upload Dog's Photo", type=["jpg", "jpeg", "png"])
        
        if st.button("Add Dog", key="add_dog_btn"):
            if name and breed and address and photo:
                if add_dog(name, breed, address, age, photo):
                    st.success("🎉 Dog added successfully!")
                else:
                    st.error("😞 Failed to add dog. Please try again.")
            else:
                st.warning("🚨 Please fill in all fields and upload a photo.")
    
    # Search and filter
    search = st.text_input("🔍 Search by name, breed, or location")
    
    # Display dogs
    st.markdown('<h2 class="section-header">Find Your Furry Companion</h2>', unsafe_allow_html=True)
    
    page = st.session_state.get("page", 1)
    dogs, total_dogs = get_dogs(search, page)
    
    if not dogs:
        st.info("🐾 No dogs available right now. Check back soon or add a dog to get started!")
    else:
        # Create a grid to display dogs
        dog_columns = st.columns(3)
        for idx, dog in enumerate(dogs):
            with dog_columns[idx % 3]:
                st.markdown(f"""
                    <div class="dog-card">
                        <img src="{dog[5]}" alt="{dog[1]}" class="dog-img"/>
                        <h3>{dog[1]}</h3>
                        <p><strong>Breed:</strong> {dog[2]}</p>
                        <p><strong>Age:</strong> {dog[4]} years</p>
                        <p><strong>Location:</strong> {dog[3]}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Adopt Me! 💖", key=f"adopt_{dog[0]}"):
                    st.balloons()
                    st.success(f"🎊 Congratulations on adopting {dog[1]}! 🐶")
                    adopt_dog(dog[0])
                    st.experimental_rerun()
    
    # Pagination
    total_pages = (total_dogs - 1) // 6 + 1
    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("◀ Previous") and page > 1:
                st.session_state.page = page - 1
                st.experimental_rerun()
        with col2:
            st.markdown(f"<p class='pagination'>Page {page} of {total_pages}</p>", unsafe_allow_html=True)
        with col3:
            if st.button("Next ▶") and page < total_pages:
                st.session_state.page = page + 1
                st.experimental_rerun()
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>© 2024 Paws & Purrs Adoption. Made with 💙 for dogs and their humans.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()