import React from 'react';

// This component uses the new CSS classes we added to HomePage.css

export default function QuestionCard({
  questionId,
  questionText,
  options,
  onSelect,
  selectedValue,
}) {
  return (
    <div className="question-card">
      <p className="question-card-text">{questionText}</p>
      <div className="question-options">
        {options.map((option, index) => (
          <label
            key={index}
            // The 'selected' class is added conditionally
            className={`question-option ${selectedValue === option ? 'selected' : ''}`}
          >
            <input
              type="radio"
              name={`question-${questionId}`}
              value={option}
              onChange={() => onSelect(option)}
              // Hide the default radio button
              style={{ display: 'none' }} 
            />
            {option}
          </label>
        ))}
      </div>
    </div>
  );
}