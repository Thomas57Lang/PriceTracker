import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'
import './index.css'

let productData = []

async function getData() {
  const response = await fetch('http://localhost:8000/')
  const data = await response.json()
  console.log(data)
  return data
}

async function showPage() {
  productData = await getData();
  ReactDOM.render(<App productData={productData}/>, document.getElementById('root'))
}

showPage();