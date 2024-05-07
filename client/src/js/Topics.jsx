import React, { useState } from "react";

import { Container } from "react-bootstrap";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";

import JournalNav from "./components/navbar";
import ChatBot from "./components/chat";

function Topics() {
  const [topics, setTopics] = useState([]);

  function renderEventContent(eventInfo) {
    const topicToColor = {
      Exercise: "#FF6347",
      Family: "#4169E1",
      Food: "#32CD32",
      Friends: "#FFD700",
      God: "#663399",
      Health: "#00CED1",
      Love: "#FF69B4",
      Recreation: "#808080",
      School: "#4682B4",
      Sleep: "#9370DB",
      Work: "#FFA500",
    };

    const color = topicToColor[eventInfo.event.title];

    return (
      <div style={{ backgroundColor: color }}>{eventInfo.event.title}</div>
    );
  }

  const handleDatesSet = (info) => {
    const startDate = info.startStr;
    const endDate = info.endStr;

    const uuid = localStorage.getItem("uuid");

    fetch(
      `/api/topics_between_dates?start_date=${startDate}&end_date=${endDate}`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json", UUID: uuid },
      }
    )
      .then((response) => response.json())
      .then((data) => setTopics(data))
      .catch((error) => console.error("Error fetching topics:", error));
  };

  return (
    <Container>
      <JournalNav />
      <Container className={"mt-4"}>
        <FullCalendar
          plugins={[dayGridPlugin]}
          initialView="dayGridMonth"
          weekends={true}
          events={topics}
          eventContent={renderEventContent}
          datesSet={handleDatesSet}
        />
      </Container>
      {/* <ChatBot /> */}
    </Container>
  );
}

export default Topics;
