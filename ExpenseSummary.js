// components/ExpenseSummary.js
import React from 'react';

const ExpenseSummary = ({ expenses }) => {
  const totalExpenses = expenses.reduce((sum, expense) => sum + expense.amount, 0);
  const averageExpense = expenses.length > 0 ? totalExpenses / expenses.length : 0;

  return (
    <div className="expense-summary">
      <h2>Summary</h2>
      <p>Total Expenses: ${totalExpenses.toFixed(2)}</p>
      <p>Number of Expenses: {expenses.length}</p>
      <p>Average Expense: ${averageExpense.toFixed(2)}</p>
    </div>
  );
};

export default ExpenseSummary;