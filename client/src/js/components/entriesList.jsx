import React from 'react'
import ReactDOM from 'react-dom/client'

import ListGroup from 'react-bootstrap/ListGroup';

function EntriesList() {
  return (
    <ListGroup>
      <ListGroup.Item active>May 5, 2024</ListGroup.Item>
      <ListGroup.Item>May 4, 2024</ListGroup.Item>
      <ListGroup.Item>May 3, 2024</ListGroup.Item>
      <ListGroup.Item>May 2, 2024</ListGroup.Item>
      <ListGroup.Item>May 1, 2024</ListGroup.Item>
    </ListGroup>
  )
}

export default EntriesList;



