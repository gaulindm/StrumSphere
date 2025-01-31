from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics import renderPDF
from reportlab.platypus import SimpleDocTemplate, Paragraph,Flowable, Table, TableStyle, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from django.conf import settings
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
import json
import os
import re
from .chord_utils import load_chords, extract_used_chords, draw_footer, ChordDiagram

def generate_songs_pdf(response, songs, user):
    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        topMargin=2,
        bottomMargin=80,
        leftMargin=20,
        rightMargin=20,
    )
    styles = getSampleStyleSheet()
    base_style = styles['BodyText']
    bridge_style = ParagraphStyle('Chorus', parent=base_style, fontSize=13, leading=14, spaceBefore=12, spaceAfter=12, alignment=1)
    chorus_style = ParagraphStyle('Chorus', parent=base_style, fontSize=13, leading=14, spaceBefore=12, spaceAfter=12, alignment=1)
    verse_style = ParagraphStyle('Verse', parent=base_style, fontSize=13, leading=14, spaceBefore=12, spaceAfter=12)

    elements = []



    # Get user preferences
    instrument = user.userpreference.instrument
    is_lefty = user.userpreference.is_lefty
    is_printing_alternate_chord = user.userpreference.is_printing_alternate_chord


    # Load chords and extract relevant ones
    chords = load_chords(instrument)
    used_chords = extract_used_chords(songs[0].lyrics_with_chords)  # Assuming one song for simplicity
    relevant_chords = [chord for chord in chords if chord["name"].lower() in map(str.lower, used_chords)]

    diagrams_to_draw = []
    for chord in relevant_chords:
        diagrams_to_draw.append({
            "name": chord["name"],
            "variation": chord["variations"][0]
        })
        if is_printing_alternate_chord and len(chord["variations"]) > 1:
            diagrams_to_draw.append({
                "name": chord["name"],
                "variation": chord["variations"][1]
            })


    # Calculate diagrams per row and rows needed
    chord_spacing = 50 if instrument == "ukulele" else 70  # Adjust spacing per instrument
    page_width, page_height = letter
    max_chords_per_row = int((page_width - 2 * doc.leftMargin) / chord_spacing)
    total_diagrams = len(relevant_chords) * (2 if len(relevant_chords) < 7 else 1)  # Include 2 variations if < 7 chords
    rows_needed = (total_diagrams + max_chords_per_row - 1) // max_chords_per_row  # Calculate rows needed

    row_spacing = 72  # Space between rows
    diagram_height = rows_needed * row_spacing

    # Adjust bottom margin dynamically
    if rows_needed > 1:
        doc.bottomMargin = max(80, diagram_height + 20)  # Ensure there's enough space for diagrams

    # Debugging output
    print(f"Total diagrams: {total_diagrams}, Rows needed: {rows_needed}, Bottom margin: {doc.bottomMargin}")



    songwriter_style = ParagraphStyle(
        'SongwriterStyle',
        parent=styles['Normal'],  # Inherit other properties from the Normal style
        alignment=1,  # Center alignment
        fontSize=14,  # Adjust size if needed
        spaceBefore=6,
        spaceAfter=6
    )

    recording_style = ParagraphStyle(
        'RecordingStyle',
        parent=styles['Normal'],  # Inherit other properties from the Normal style
        alignment=1,  # Center alignment
        fontSize=13,  # Adjust size if needed
        spaceBefore=6,
        spaceAfter=6
    )

    first_vocal_note_style = ParagraphStyle(
        'FirstVocalNoteStyle',
        parent=styles['Normal'],  # Inherit from the Normal style
        alignment=2,  # Right-aligned text
        fontSize=12,  # Optional: Adjust the font size
        spaceBefore=6,  # Optional: Add space above the paragraph
        spaceAfter=6,  # Optional: Add space below the paragraph
    )

    for song in songs:
        #preferences = user.userpreference
        instrument = user.userpreference.instrument
        is_lefty = user.userpreference.is_lefty

        chords = load_chords(instrument)
        used_chords = extract_used_chords(song.lyrics_with_chords)
        relevant_chords = [chord for chord in chords if chord["name"].lower() in map(str.lower, used_chords)]

  




        # Header Section
        metadata = song.metadata or {}
        artist = metadata.get('artist', 'Unknown Artist')
        album = metadata.get('album', 'Unknown')
        songwriter = metadata.get('songwriter', 'Unknown')
        year = metadata.get('year', 'Unknown')
        recording = metadata.get('recording', 'Unknown')

        #song = type('Song', (object,), {'songTitle': "Hey, Good Lookin'"})

       # metadata_text = f"""
       # <b>Artist:</b> {metadata.get('artist', 'Unknown Artist')}<br/>
       # <b>Album:</b> {metadata.get('album', 'Unknown')}<br/>
       # <b>Year:</b> {metadata.get('year', 'Unknown')}<br/>
       # <b>Chords Match YouTube Pitch:</b> {metadata.get('chords_match', 'N/A')}
       # """



        recorded_by_text = f"{metadata.get('recording', 'Unknown')} recording by {metadata.get('artist', 'Unknown Artist')}"
        #if metadata.get('album', ''):
        #    recorded_by_text += f" on {metadata['album']}"
        if metadata.get('year', ''):
            recorded_by_text += f" in {metadata['year']}"

        header_data = [
            [
                Paragraph(f"{metadata.get('timeSignature', '')}", styles['Normal']),
                Paragraph(f"<b>{song.songTitle or 'Untitled Song'}</b>", styles['Title']),
                Paragraph(f"First Vocal Note: {metadata.get('1stnote', 'N/A')}", first_vocal_note_style),
            ],
            [
               # Paragraph(f"Tempo: {metadata.get('tempo', '')}", styles['Normal']),    Uncertain of style to adopt
                Paragraph(f"{metadata.get('songwriter', '')}", songwriter_style),  # Ensure style is correct
                "",
                "",
            ],
            [
                Paragraph(recorded_by_text, recording_style),
                "",
                "",
            ],
        ]

        header_table = Table(header_data, colWidths=[120, 360, 120])
        header_table.setStyle(TableStyle([
            ('SPAN', (0, 1), (2, 1)),  # Merge all three cells in the second row
            ('SPAN', (0, 2), (2, 2)),  # Merge all three cells in the third row
            
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells as a base
            ('VALIGN', (1, 1), (1, 1), 'MIDDLE'),  # Specifically center align the songwriter cell
            ('LEFTPADDING', (1, 1), (1, 1), 10),
            ('RIGHTPADDING', (1, 1), (1, 1), 10),
            ('TOPPADDING', (1, 1), (2, 2), 0),
            ('BOTTOMPADDING', (1, 1), (1, 1), 5),
            #('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines for debugging
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 12))

      # Lyrics Section with section handling
        lyrics_with_chords = song.lyrics_with_chords or []
        paragraph_buffer = []
        chorus_line_buffer = []
        is_chorus = False
        refrain_added = False

        for group in lyrics_with_chords:
            for item in group:
                if "directive" in item:
                    if item["directive"] == "{soc}":
                        is_chorus = True
                        if paragraph_buffer:
                            elements.append(Paragraph(" ".join(paragraph_buffer), verse_style))
                            paragraph_buffer = []

                        # Reset the chorus table structure
                        chorus_table_data = []
                        chorus_line_buffer = []  # Buffer to accumulate a full line before adding to the table
                        continue  # Move to the next item

                    elif item["directive"] == "{eoc}":
                        is_chorus = False
                        
                        if chorus_line_buffer:  # Make sure we store the final buffer before EOC
                            full_line = " ".join(chorus_line_buffer)
                            chorus_table_data.append(["", Paragraph(full_line, chorus_style)])

                        if chorus_table_data:  # Ensure "Refrain:" is always the first row
                            
                            chorus_table_data.insert(0, [
                                Paragraph("<b>Refrain:</b>", ParagraphStyle(
                                    'RefrainStyle',
                                    parent=chorus_style,
                                    alignment=0,
                                    fontSize=13,
                                    leading=14,
                                    spaceBefore=2,
                                    spaceAfter=2,
                                    textColor=colors.black
                                )),
                                chorus_table_data.pop(0)[1] if chorus_table_data else Paragraph("", chorus_style)
                            ])

                            # Create the chorus table
                            chorus_table = Table(chorus_table_data, colWidths=[80, 440], hAlign='LEFT')
                            chorus_table.setStyle(TableStyle([
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                                #('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ]))

                            elements.append(chorus_table)
                            elements.append(Spacer(1, 12))  # Space after chorus

                        # Reset buffer after processing chorus
                        chorus_line_buffer = []
            




                elif "format" in item:
                    if item["format"] == "LINEBREAK":
                        if is_chorus and chorus_line_buffer:
                            # Store full chorus line before resetting buffer
                            full_line = " ".join(chorus_line_buffer)
                            chorus_table_data.append(["", Paragraph(full_line, chorus_style)])

                            # Reset buffer only after storing full line
                            chorus_line_buffer = []   

                        elif not is_chorus and paragraph_buffer:
                            paragraph_buffer.append("<br/>")  # Keep verse formatting

                    elif item["format"] == "PARAGRAPHBREAK":
                        if paragraph_buffer:
                            paragraph_text = " ".join(paragraph_buffer)
                            style = chorus_style if is_chorus else verse_style
                            elements.append(Paragraph(paragraph_text, style))
                            paragraph_buffer = []  # Reset buffer

                elif "lyric" in item:
                    chord = item.get("chord", "")
                    lyric = item["lyric"]
                    line = f"<b>[{chord}]</b> {lyric}" if chord else lyric

                    if is_chorus:
                        chorus_line_buffer.append(line)  # Accumulate chorus lines until a LINEBREAK
                        
                    else:
                        paragraph_buffer.append(line)  # Accumulate verse lines as usual


        # Add remaining lines
        if paragraph_buffer:
            paragraph_text = " ".join(paragraph_buffer)
            style = chorus_style if is_chorus else verse_style
            elements.append(Paragraph(paragraph_text, style))
            paragraph_buffer = []

        elements.append(PageBreak())  # Separate songs by page

    # Define spacing and build the document
    page_width, page_height = letter
    available_width = page_width - 2 * doc.leftMargin
    max_chords_per_row = 8
    chord_spacing = available_width / max_chords_per_row
    row_spacing = 72

    doc.build(
        elements,
        onFirstPage=lambda c, d: draw_footer(
            c, d, relevant_chords, chord_spacing, row_spacing, is_lefty,
            instrument=instrument,
            is_printing_alternate_chord=user.userpreference.is_printing_alternate_chord
        ),
        onLaterPages=lambda c, d: draw_footer(
            c, d, relevant_chords, chord_spacing, row_spacing, is_lefty,
            instrument=instrument,
            is_printing_alternate_chord=user.userpreference.is_printing_alternate_chord
        )
    )
