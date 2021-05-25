import cv2
import numpy as np

from app.package.services import imbasic as imb


def print_instructions():
    msg = '''
    ** Instrucciones **
    - Uso de las teclas [+] [-] para aumentar el valor de "alpha"
    - Se dibujará en la pantalla un rectángulo
    - Este rectángulo tendrá el color que tenga una de las rejillas en
      la pantalla de adquisición de datos cuando el micrófono haya pasado
      alpha (definido en el rango [0, 1])

    '''
    print(msg)


def draw_overlay(frame, times):
    for t in times:
        if t < 0.5:
            # Degradado rojo -> transparente
            alpha = 0.5 - t
            imb.draw_filled_rectangle(
                frame, (0, 0), (200, 200), (0, 0, 255), alpha)

        else:
            # Degradado transparente -> verde
            alpha = t - 0.5
            imb.draw_filled_rectangle(
                frame, (0, 0), (200, 200), (0, 255, 0), alpha)

    return frame


def main():
    print_instructions()
    cap = cv2.VideoCapture(0)

    t = 0

    while True:
        t = np.clip(t, 0, 1)
        ret, frame = cap.read()

        color_frame = draw_overlay(frame, [t])

        imb.imshow(color_frame)
        key = cv2.waitKey(1)

        if key == ord('+'):
            t += 0.1
        if key == ord('-'):
            t -= 0.1
        if key == ord('q'):
            break


if __name__ == '__main__':
    main()
