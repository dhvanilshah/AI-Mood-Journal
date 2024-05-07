import React, { useState, useEffect } from "react";

import { Container, ListGroup, Pagination } from "react-bootstrap";

const itemsPerPage = 12;

function EntriesList({ notes, onSelect, selectedNote }) {
  const [currentPage, setCurrentPage] = useState(1);

  if (notes == undefined || notes.length === 0) {
    return <div>No items available.</div>;
  }

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = notes.slice(indexOfFirstItem, indexOfLastItem);

  const totalPages = Math.ceil(notes.length / itemsPerPage);

  const paginate = (pageNumber) => {
    onSelect(null);
    setCurrentPage(pageNumber);
  };

  const reformatDateString = (dateString) => {
    // Create a new Date object from the input date string
    const date = new Date(dateString);

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

  const onNoteSelect = (note) => {
    if (selectedNote?.id == note.id) {
      onSelect(null);
    } else {
      onSelect(note);
    }
  };

  return (
    <div>
      <ListGroup>
        {currentItems.map((item, index) => (
          <ListGroup.Item
            action
            key={item.id}
            onClick={() => onNoteSelect(item)}
            active={selectedNote?.id == item.id}
          >
            {reformatDateString(item.date)}
          </ListGroup.Item>
        ))}
      </ListGroup>
      <Pagination className="mt-2">
        {Array.from({ length: totalPages }).map((_, index) => (
          <Pagination.Item
            key={index}
            active={index + 1 === currentPage}
            onClick={() => paginate(index + 1)}
          >
            {index + 1}
          </Pagination.Item>
        ))}
      </Pagination>
    </div>
  );
}

export default EntriesList;
