import React from 'react'

function captions({ captions }) {
  return (
    <ul>
      {captions.map((caption) => (
        <li key={caption.startTime}>
          {caption.startTime} - {caption.endTime}: {caption.text}
        </li>
      ))}
    </ul>
  )
}

export default captions;