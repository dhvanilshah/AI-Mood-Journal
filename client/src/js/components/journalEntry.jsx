import React from 'react'
import ReactDOM from 'react-dom/client'

import Card from 'react-bootstrap/Card';

function JournalEntry() {
  return (
    <Card style={{ width: '100%' }}>
      <Card.Body>
        <Card.Title>May 5, 2024</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">Saved 11:55pm</Card.Subtitle>
        <Card.Text>
          This is an example of a journal entry. Today I was feeling good. I ate food. I write code. I have bag.
          Bag was leaky. There was water in my bag. My bad dye stained my shirt. I was feeling not so good. But, then, I
          ate more food. So again, I was good.
        </Card.Text>
      </Card.Body>
    </Card>
  )
}

export default JournalEntry;



