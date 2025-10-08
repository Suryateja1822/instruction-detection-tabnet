import streamlit as st
import numpy as np
import os
from pytorch_tabnet.tab_model import TabNetClassifier

def preprocess_text(texts):
    """Preprocess text input for prediction"""
    return [str(text).lower() for text in texts]

def get_char_frequencies(texts):
    """Extract character frequency features"""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789 ,.!?'
    char_to_idx = {c: i for i, c in enumerate(chars)}
    
    features = np.zeros((len(texts), len(chars)))
    
    for i, text in enumerate(texts):
        for c in str(text).lower():
            if c in char_to_idx:
                features[i, char_to_idx[c]] += 1
        
        if len(str(text)) > 0:
            features[i] /= len(str(text))
            
    return features

@st.cache_resource
def load_model():
    """Load the trained TabNet model"""
    model_path = "models/tabnet_instruction_model.zip"
    if not os.path.exists(model_path):
        return None
    
    clf = TabNetClassifier()
    clf.load_model(model_path)
    return clf

def main():
    st.set_page_config(
        page_title="Instruction Detection using TabNet",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Instruction Detection using TabNet")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("About")
    st.sidebar.info(
        "This application uses TabNet, a deep learning architecture "
        "for tabular data, to classify different types of instructions."
    )
    
    st.sidebar.header("Instruction Classes")
    classes = [
        "action_device - Device control commands",
        "action_list - List management",
        "action_media - Media playback",
        "action_reminder - Reminder setting",
        "action_timer - Timer/alarm setting",
        "query_calendar - Calendar queries",
        "query_date - Date queries",
        "query_time - Time queries",
        "query_weather - Weather queries"
    ]
    for cls in classes:
        st.sidebar.text(f"• {cls}")
    
    # Main content
    model = load_model()
    
    if model is None:
        st.error("⚠️ Model not found! Please train the model first using `python src/train.py`")
        return
    
    st.success("✅ Model loaded successfully!")
    
    # Input methods
    tab1, tab2 = st.tabs(["Single Instruction", "Batch Instructions"])
    
    with tab1:
        st.subheader("Classify a Single Instruction")
        
        instruction = st.text_input(
            "Enter an instruction:",
            placeholder="e.g., Turn on the lights"
        )
        
        if st.button("Classify", key="single"):
            if instruction:
                with st.spinner("Classifying..."):
                    # Preprocess and predict
                    processed = preprocess_text([instruction])
                    features = get_char_frequencies(processed)
                    prediction = model.predict(features)[0]
                    
                    # Display result
                    st.markdown("### Result")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Instruction", instruction)
                    
                    with col2:
                        st.metric("Predicted Class", prediction)
            else:
                st.warning("Please enter an instruction first!")
    
    with tab2:
        st.subheader("Classify Multiple Instructions")
        
        instructions_text = st.text_area(
            "Enter instructions (one per line):",
            placeholder="Turn on the lights\nWhat's the weather?\nSet a timer for 5 minutes",
            height=200
        )
        
        if st.button("Classify All", key="batch"):
            if instructions_text:
                instructions = [line.strip() for line in instructions_text.split('\n') if line.strip()]
                
                if instructions:
                    with st.spinner("Classifying..."):
                        # Preprocess and predict
                        processed = preprocess_text(instructions)
                        features = get_char_frequencies(processed)
                        predictions = model.predict(features)
                        
                        # Display results in a table
                        st.markdown("### Results")
                        results_df = {
                            "Instruction": instructions,
                            "Predicted Class": predictions
                        }
                        
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Download button
                        import pandas as pd
                        df = pd.DataFrame(results_df)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name="instruction_predictions.csv",
                            mime="text/csv"
                        )
                else:
                    st.warning("Please enter at least one instruction!")
            else:
                st.warning("Please enter instructions first!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center'>"
        "<p>Built with Streamlit and TabNet</p>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
