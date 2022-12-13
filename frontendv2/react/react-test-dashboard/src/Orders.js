import * as React from 'react';
// import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Title from './Title';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Popover from '@mui/material/Popover';

async function getItemData(sku, table) {
  const response = await fetch('http://localhost:8000/item/?table_name=' + table + '&sku=' + sku);
  const data = await response.json();
  return data[0];
}

async function handleText(asiSKU, ingramSKU) {
  if (asiSKU !== "") {
    const itemData = await getItemData(asiSKU, "ASIItem");
    //console.log(itemData);
    return itemData;
  }
  else if (ingramSKU !== "") {
    const itemData = await getItemData(ingramSKU, "IngramItem");
    //console.log(itemData);
    return itemData;
  }
  return "";
}

export default function Orders({rows = []}) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [popoverText, setPopoverText] = React.useState("");

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handlePopover = (asiSKU, ingramSKU) => {
    const itemData = handleText(asiSKU, ingramSKU);
    itemData.then((val) => {
      console.log(val);
      setPopoverText("Item SKU: " + val.itemSKU + " Price: " + val.price + " Stock: " + val.stock);
    })
  }
  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

 
  return (
    <React.Fragment>
    <Popover
      id={id}
      open={open}
      anchorEl={anchorEl}
      onClose={handleClose}
      anchorOrigin={{
        vertical: 'bottom',
        horizontal: 'left',
      }}
    >
      <Typography sx={{ p: 2 }}>{popoverText}</Typography>
    </Popover>
      <Title>Products</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Item Name</TableCell>
            <TableCell>Part #</TableCell>
            <TableCell>Description</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.partnum}>
              <TableCell>
                <Stack spacing={2} direction="row">
                  <Button aria-describedby={id} variant="text" 
                  onClick={(e) => {
                    handleClick(e);
                    handlePopover(row.asiSKU, row.ingramSKU);
                  }}>
                    {row.itemName}
                  </Button>
                </Stack>
              </TableCell>
              <TableCell>{row.partnum}</TableCell>
              <TableCell>{row.partdescription}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </React.Fragment>
  );
}