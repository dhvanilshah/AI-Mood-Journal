import React from 'react'
import ReactDOM from 'react-dom/client'

import { Container } from 'react-bootstrap';
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'

import JournalNav from './components/navbar'
import ChatBot from './components/chat'

function Moods() {
    const events = [
      { title: 'Happy',
      start: "2024-05-01",
      end: "2024-05-04",
      className: "success"
      }
    ]

    function renderEventContent(eventInfo) {
      return (
        <>
          <b>{eventInfo.event.title}</b>
        </>
      )
    }

  return (
      <Container>
        <JournalNav />
        <Container className={'mt-4'}>
        <FullCalendar
          plugins={[dayGridPlugin]}
          initialView='dayGridMonth'
          weekends={true}
          events={events}
          eventContent={renderEventContent}
        />
        </Container>
        <ChatBot />
      </Container>
)
}

export default Moods;



