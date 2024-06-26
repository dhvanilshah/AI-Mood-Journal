import React, { useState } from "react";

import { Container } from "react-bootstrap";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";

import JournalNav from "./components/navbar";
import ChatBot from "./components/chat";

function Moods() {
  const [moods, setMoods] = useState([]);

  function renderEventContent(eventInfo) {
    const moodToColor = {
      Afraid: "#663399",
      Angry: "#FF4500",
      Anxious: "#E5DE00",
      Ashamed: "#CD5C5C",
      Awkward: "#808080",
      Bored: "#A9A9A9",
      Calm: "#00CED1",
      Confused: "#9370DB",
      Disgusted: "#8B4513",
      Excited: "#FFD700",
      Frustrated: "#FF6347",
      Happy: "#FFD700",
      Jealous: "#32CD32",
      Nostalgic: "#D2B48C",
      Proud: "#4169E1",
      Sad: "#4682B4",
      Satisfied: "#228B22",
      Surprised: "#FFA500 ",
    };

    const color = moodToColor[eventInfo.event.title];

    return (
      <div style={{ backgroundColor: color }}>{eventInfo.event.title}</div>
    );
  }

  const handleDatesSet = (info) => {
    const startDate = info.startStr;
    const endDate = info.endStr;

    const uuid = localStorage.getItem("uuid");

    fetch(
      `/api/moods_between_dates?start_date=${startDate}&end_date=${endDate}`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json", UUID: uuid },
      }
    )
      .then((response) => response.json())
      .then((data) => setMoods(data))
      .catch((error) => console.error("Error fetching moods:", error));
  };

  return (
    <Container>
      <JournalNav />
      <Container className={"mt-4"}>
        <FullCalendar
          plugins={[dayGridPlugin]}
          initialView="dayGridMonth"
          weekends={true}
          events={moods}
          eventContent={renderEventContent}
          datesSet={handleDatesSet}
        />
      </Container>
      {/* <ChatBot /> */}
    </Container>
  );
}

export default Moods;
