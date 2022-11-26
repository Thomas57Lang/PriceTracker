import React, { Component } from 'react'
import Products from './Products'

class App extends React.Component {
    render() {
        const { productData } = this.props
        return (
            <div className="container">
                <Products productData={productData}/>
            </div>
        )
    }
}

export default App