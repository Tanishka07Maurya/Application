import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import FormInput from '../components/forms/FormInput';
import Button from '../components/forms/Button';
import { addQuestion, updateQuestion, fetchQuestions } from '../api/apiService';

export default function EditQuestionPage({ isNew }) {
  const { questionId } = useParams();

  const [formData, setFormData] = useState({ 
    text: '', 
    options: ['', '', '', ''], 
    correct: '' 
  });

  // 1. Load Data on Edit
  useEffect(() => {
    if (!isNew && questionId) {
      const loadQuestion = async () => {
        try {
          const res = await fetchQuestions();
          const q = res.data.find((item) => item.id === parseInt(questionId));
          if (q) {
            const loadedOptions = q.options || [];
            while (loadedOptions.length < 4) loadedOptions.push("");

            const correctIndex = loadedOptions.indexOf(q.correct);

            setFormData({
              text: q.text,
              options: loadedOptions,
              correct: correctIndex > -1 ? correctIndex.toString() : '', 
            });
          }
        } catch (err) {
          console.error(err);
        }
      };
      loadQuestion();
    }
  }, [isNew, questionId]);

  // 2. Input Handlers
  const handleTextChange = (e) => {
    setFormData({ ...formData, text: e.target.value });
  };

  const handleOptionChange = (index, value) => {
    const newOptions = [...formData.options];
    newOptions[index] = value;
    setFormData({ ...formData, options: newOptions });
  };

  const handleCorrectChange = (e) => {
    setFormData({ ...formData, correct: e.target.value });
  };

  // 3. Updated Handle Submit (Strict Validation)
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const cleanOptions = formData.options.filter(opt => opt.trim() !== "");

    if(cleanOptions.length < 2) {
        alert("Please provide at least 2 options.");
        return;
    }
    if(formData.correct === '') {
        alert("Please select which option is the correct answer.");
        return;
    }
    // ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    const dataToSend = {
        text: formData.text, 
        options: cleanOptions, 
        correct_index: formData.correct, 
        question_type: 'MCQ',
        unit: 1, 
        marks: 1, 
    };

    try {
        const response = await addQuestion(dataToSend); 
        alert("Question saved successfully!");
    } catch (error) {
        console.error("Failed to add question:", error.response ? error.response.data : error.message);
        alert("Error saving question. Please try again.");
    }
    // ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
  };

  return (
    // ✅ THIS IS THE LINE THAT CENTERS THE CARD
    <main className="main-content" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      
      <div className="card form-container">
        <form onSubmit={handleSubmit}>
          <h2 className="page-title">
            {isNew ? 'Add New Question' : 'Edit Question'}
          </h2>

          {/* Question Text */}
          <FormInput 
            label="Question Text" 
            name="text" 
            value={formData.text} 
            onChange={handleTextChange} 
            required 
          />

          <h4 style={{marginTop: '20px', marginBottom: '10px'}}>Options</h4>
          
          {/* Loop to create 4 Input Boxes */}
          {formData.options.map((option, index) => (
            <FormInput
              key={index}
              label={`Option ${index + 1}`}
              name={`option-${index}`}
              value={option}
              onChange={(e) => handleOptionChange(index, e.target.value)}
              required 
            />
          ))}

          {/* Dropdown */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Correct Answer
            </label>
            <select
              value={formData.correct}
              onChange={handleCorrectChange}
              required
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '5px',
                border: '1px solid #ccc',
                backgroundColor: '#fff'
              }}
            >
              <option value="">-- Select Correct Answer --</option>
              
              {/* Options 1-4 Dropdown */}
              {formData.options.map((_, index) => (
                 <option key={index} value={index}>
                    Option {index + 1}
                 </option>
              ))}
            </select>
          </div>

          <Button
            type="submit"
            label="Save Question"
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '1rem' }}
          />
        </form>
      </div>
    </main>
  );
}
