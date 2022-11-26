import React, { Component } from 'react'

const TableHeader = () => {
    return (
        <thead>
        <tr>
            <th>ItemSKU</th>
            <th>Price</th>
            <th>Stock</th>
        </tr>
        </thead>
    )
}

const TableBody = (props) => {
    const rows = props.productData.map((row, index) => {
        return (
            <tr key={index}>
                <td>{row.itemSKU}</td>
                <td>{row.price}</td>
                <td>{row.stock}</td>
            </tr>
        )
    })
    return <tbody>{rows}</tbody>
}

class Products extends Component {
    render() {
        const { productData } = this.props
        console.log(this.props)
        return (
            <table>
                <TableHeader />
                <TableBody productData={productData}/>
            </table>
        )
    }
}

export default Products