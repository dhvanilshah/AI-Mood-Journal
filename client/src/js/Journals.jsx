import React from "react";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import { Button, Container, Row, Col } from "react-bootstrap";

import JournalNav from './components/navbar'
import EntriesList from './components/entriesList'
import JournalEntry from './components/journalEntry'
import ChatBot from './components/chat'

export default class App extends React.Component {
  render() {
    return (
      <Container>
        <JournalNav />
        <Row className={'mt-4 mb-2'}>
            <Col xs={4} sm={4} md={4} lg={4} style={{display:'flex', justifyContent:'right'}}>
              <Button> New Entry </Button>
            </Col>
            <Col xs={8} sm={8} md={8} lg={8} style={{display:'flex', justifyContent:'right'}}>
              <Button> Edit </Button>
            </Col>
        </Row>
        <Row className={'mt-2'}>
            <Col xs={4} sm={4} md={4} lg={4}>
              <EntriesList />
            </Col>
            <Col xs={8} sm={8} md={8} lg={8}>
              <JournalEntry />
            </Col>
        </Row>
        <ChatBot />
      </Container>
    );
  }
}
