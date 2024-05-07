import React from "react";
import ReactDOM from "react-dom/client";

import Card from "react-bootstrap/Card";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

function JournalEntry({ note, isEdit, onNoteChange, onDeleteClick }) {
  const getDateString = (dateString) => {
    // Create a new Date object from the input date string
    const date = dateString == "" ? new Date() : new Date(dateString);

    // Array of month names
    const months = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];

    // Get the month, day, and year from the date object
    const month = months[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();

    // Concatenate the formatted date
    const formattedDate = `${month} ${day}, ${year}`;

    return formattedDate;
  };

  const reformatTimeString = (dateString) => {
    // Create a new Date object from the input date string
    const date = new Date(dateString);

    // Extract hours, minutes, and AM/PM
    const hours = date.getHours() % 12 || 12; // Convert 0 to 12 for 12-hour format
    const minutes = ("0" + date.getMinutes()).slice(-2); // Ensure two digits
    const period = date.getHours() < 12 ? "am" : "pm"; // Determine AM/PM

    // Concatenate the formatted time
    const formattedTime = `${hours}:${minutes} ${period}`;

    return formattedTime;
  };

  if (isEdit) {
    return (
      <Card.Body>
        <Card.Title>{getDateString("")}</Card.Title>
        <Card.Text>
          <Form.Control
            as="textarea"
            rows={5}
            className="my-2"
            placeholder="Add your journal entry..."
            onChange={(e) => onNoteChange(e)}
          />
        </Card.Text>
      </Card.Body>
    );
  }

  if (note == null && !isEdit) {
    return (
      <Card style={{ width: "100%" }}>
        <Card.Body>
          <Card.Text>Please select a journal entry to view.</Card.Text>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card style={{ width: "100%" }}>
      <Card.Body>
        <Card.Title>{getDateString(note.date)}</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">
          Saved {reformatTimeString(note.date)}
        </Card.Subtitle>
        <Card.Text>{note.note}</Card.Text>
        <Button variant="danger" onClick={onDeleteClick}>
          Delete
        </Button>
      </Card.Body>
    </Card>
  );
}

export default JournalEntry;
