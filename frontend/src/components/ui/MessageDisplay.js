import React from 'react';

export default function MessageDisplay({ message, type }) {
  if (!message) return null;
  return <div className={`message-display ${type}`}>{message}</div>;
}