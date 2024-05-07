import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import { Button, Container, Row, Col } from "react-bootstrap";

import JournalNav from "./components/navbar";
import EntriesList from "./components/entriesList";
import JournalEntry from "./components/journalEntry";
import ChatBot from "./components/chat";

function Journals() {
  const [entries, setEntries] = useState([]);
  const [isEdit, setIsEdit] = useState(false);
  const [selectedNote, setSelectedNote] = useState(null);
  const [editText, setEditText] = useState("");

  const fetchData = async () => {
    const uuid = localStorage.getItem("uuid");
    const res = await fetch("/api/posts", {
      method: "GET",
      headers: { "Content-Type": "application/json", UUID: uuid },
    });
    const data = await res.json();
    if (data.error) {
      alert(data.error);
    } else {
      const posts = data.posts;

      const sortedPosts = posts.sort((a, b) => {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        return dateB - dateA;
      });

      setEntries(sortedPosts);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onNoteSelect = (note) => {
    setSelectedNote(note);
  };

  const onNewNote = () => {
    setIsEdit(true);
    setSelectedNote(null);
  };

  const onCancel = () => {
    setIsEdit(false);
    setSelectedNote(null);
  };

  const onNoteChange = (e) => {
    const text = e.target.value;
    setEditText(text);
  };

  const onNoteSave = async () => {
    const uuid = localStorage.getItem("uuid");
    const res = await fetch("/api/new_post", {
      method: "POST",
      headers: { "Content-Type": "application/json", UUID: uuid },
      body: JSON.stringify({
        note: editText,
      }),
    });
    const data = await res.json();
    if (data.note) {
      setEditText(null);
      setIsEdit(false);
      setSelectedNote(null);
      fetchData();
    }
  };

  const onNoteDelete = async () => {
    const uuid = localStorage.getItem("uuid");
    const res = await fetch("/api/delete_post", {
      method: "POST",
      headers: { "Content-Type": "application/json", UUID: uuid },
      body: JSON.stringify({
        note_id: selectedNote.id,
      }),
    });
    const data = await res.json();
    if (data.note_id == selectedNote.id) {
      setSelectedNote(null);
      fetchData();
    }
  };

  return (
    <Container>
      <JournalNav />
      <Row className={"mt-4 mb-2"}>
        <Col
          xs={4}
          sm={4}
          md={4}
          lg={4}
          style={{ display: "flex", justifyContent: "right" }}
        >
          <Button onClick={() => onNewNote()} disabled={isEdit}>
            New Entry
          </Button>
        </Col>
        <Col
          xs={8}
          sm={8}
          md={8}
          lg={8}
          style={{ display: "flex", justifyContent: "right" }}
        >
          {isEdit && (
            <>
              <Button variant="danger" className="mx-2" onClick={onCancel}>
                Cancel
              </Button>
              <Button variant="success" onClick={onNoteSave}>
                Save
              </Button>
            </>
          )}
        </Col>
      </Row>
      <Row className={"mt-2"}>
        <Col xs={4} sm={4} md={4} lg={4}>
          <EntriesList
            notes={entries}
            onSelect={onNoteSelect}
            selectedNote={selectedNote}
          />
        </Col>
        <Col xs={8} sm={8} md={8} lg={8}>
          <JournalEntry
            note={selectedNote}
            isEdit={isEdit}
            onNoteChange={onNoteChange}
            onDeleteClick={onNoteDelete}
          />
        </Col>
      </Row>
      {/* <ChatBot /> */}
    </Container>
  );
}

export default Journals;
