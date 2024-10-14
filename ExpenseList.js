// components/ExpenseList.js
import React from 'react';

const ExpenseList = ({ expenses, deleteExpense, setFilterCategory }) => {
  return (
    <div className="expense-list">
      <h2>Expenses</h2>
      <select onChange={(e) => setFilterCategory(e.target.value)}>
        <option value="all">All Categories</option>
        {/* Add unique categories dynamically */}
        {[...new Set(expenses.map(expense => expense.category))].map(category => (
          <option key={category} value={category}>{category}</option>
        ))}
      </select>
      <ul>
        {expenses.map((expense)=> (
          <li key={expense.id} className="expense-item">
            <span>{expense.category}</span>
            <span>${expense.amount.toFixed(2)}</span>
            <span>{new Date(expense.date).toLocaleDateString()}</span>
            <button onClick={() => deleteExpense(expense.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ExpenseList;