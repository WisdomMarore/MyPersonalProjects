// App.js
import React, { useState, useEffect } from 'react';
import ExpenseForm from './components/ExpenseForm';
import ExpenseList from './components/ExpenseList';
import ExpenseChart from './components/ExpenseChart';
import ExpenseSummary from './components/ExpenseSummary';
import './App.css';

const App = () => {
  const [expenses, setExpenses] = useState([]);
  const [filteredExpenses, setFilteredExpenses] = useState([]);
  const [filterCategory, setFilterCategory] = useState('all');

  useEffect(() => {
    const storedExpenses = JSON.parse(localStorage.getItem('expenses')) || [];
    setExpenses(storedExpenses);
    setFilteredExpenses(storedExpenses);
  }, []);

  useEffect(() => {
    localStorage.setItem('expenses', JSON.stringify(expenses));
    filterExpenses();
  }, [expenses, filterCategory]);

  const addExpense = (expense) => {
    setExpenses([...expenses, { ...expense, id: Date.now() }]);
  };

  const deleteExpense = (id) => {
    setExpenses(expenses.filter(expense => expense.id !== id));
  };

  const filterExpenses = () => {
    if (filterCategory === 'all') {
      setFilteredExpenses(expenses);
    } else {
      setFilteredExpenses(expenses.filter(expense => expense.category === filterCategory));
    }
  };

  return (
    <div className="app">
      <h1>Expense Tracker</h1>
      <ExpenseForm addExpense={addExpense} />
      <ExpenseChart expenses={filteredExpenses} />
      <ExpenseSummary expenses={filteredExpenses} />
      <ExpenseList
        expenses={filteredExpenses}
        deleteExpense={deleteExpense}
        setFilterCategory={setFilterCategory}
      />
    </div>
  );
};

export default App;