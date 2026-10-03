import face_recognition

def match_face(live_image, stored_image_path):
    known = face_recognition.load_image_file(stored_image_path)
    known_enc = face_recognition.face_encodings(known)

    if not known_enc:
        return False

    live = face_recognition.load_image_file(live_image)
    live_enc = face_recognition.face_encodings(live)

    if not live_enc:
        return False

    return face_recognition.compare_faces(
        [known_enc[0]],
        live_enc[0],
        tolerance=0.45
    )[0]
