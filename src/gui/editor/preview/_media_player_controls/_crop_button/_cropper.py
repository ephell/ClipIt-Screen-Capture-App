from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem


class Cropper(QGraphicsRectItem):

    handle_size = 12.0
    handle_space = 0
    handle_top_left = 1
    handle_top_middle = 2
    handle_top_right = 3
    handle_middle_left = 4
    handle_middle_right = 5
    handle_bottom_left = 6
    handle_bottom_middle = 7
    handle_bottom_right = 8

    handle_cursors = {
        handle_top_left: Qt.SizeFDiagCursor,
        handle_top_middle: Qt.SizeVerCursor,
        handle_top_right: Qt.SizeBDiagCursor,
        handle_middle_left: Qt.SizeHorCursor,
        handle_middle_right: Qt.SizeHorCursor,
        handle_bottom_left: Qt.SizeBDiagCursor,
        handle_bottom_middle: Qt.SizeVerCursor,
        handle_bottom_right: Qt.SizeFDiagCursor,
    }

    def __init__(self, scene, max_rect):
        super().__init__(None)
        self.scene = scene
        self.scene.addItem(self)
        self.max_rect = max_rect
        self.setRect(self.max_rect)
        self.handles = {}
        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.__update_handles_pos()

    """Override"""
    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.__handle_at(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handle_cursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    """Override"""
    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    """Override"""
    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handle_selected = self.__handle_at(mouseEvent.pos())
        if self.handle_selected:
            self.mouse_press_pos = mouseEvent.pos()
            self.mouse_press_rect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    """Override"""
    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handle_selected is not None:
            self.__resize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    """Override"""
    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None
        self.update()

    """Override"""
    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handle_size + self.handle_space
        return self.rect().adjusted(-o, -o, o, o)

    """Override"""
    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    """Override"""
    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        # painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handle_selected is None or handle == self.handle_selected:
                painter.drawEllipse(rect)

    def __handle_at(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def __update_handles_pos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handle_size
        b = self.boundingRect()
        self.handles[self.handle_top_left] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handle_top_middle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handle_top_right] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handle_middle_left] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handle_middle_right] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handle_bottom_left] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handle_bottom_middle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handle_bottom_right] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def __resize(self, mouse_pos):
        offset = self.handle_size + self.handle_space
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)
        min_size = 25
        self.prepareGeometryChange()

        if self.handle_selected == self.handle_top_left:
            fromX = self.mouse_press_rect.left()
            fromY = self.mouse_press_rect.top()
            toX = fromX + mouse_pos.x() - self.mouse_press_pos.x()
            toY = fromY + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            # Prevent overlapping.
            if rect.left() >= rect.right():
                rect.setLeft(rect.right() - min_size)
            if rect.top() >= rect.bottom():
                rect.setTop(rect.bottom() - min_size)

        elif self.handle_selected == self.handle_top_middle:
            fromY = self.mouse_press_rect.top()
            toY = fromY + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            # Prevent overlapping.
            if rect.top() >= rect.bottom():
                rect.setTop(rect.bottom() - min_size)

        elif self.handle_selected == self.handle_top_right:
            fromX = self.mouse_press_rect.right()
            fromY = self.mouse_press_rect.top()
            toX = fromX + mouse_pos.x() - self.mouse_press_pos.x()
            toY = fromY + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            # Prevent overlapping.
            if rect.right() <= rect.left():
                rect.setRight(rect.left() + min_size)
            if rect.top() >= rect.bottom():
                rect.setTop(rect.bottom() - min_size)

        elif self.handle_selected == self.handle_middle_left:
            fromX = self.mouse_press_rect.left()
            toX = fromX + mouse_pos.x() - self.mouse_press_pos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            # Prevent overlapping.
            if rect.left() >= rect.right():
                rect.setLeft(rect.right() - min_size)

        elif self.handle_selected == self.handle_middle_right:
            fromX = self.mouse_press_rect.right()
            toX = fromX + mouse_pos.x() - self.mouse_press_pos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            # Prevent overlapping.
            if rect.right() <= rect.left():
                rect.setRight(rect.left() + min_size)

        elif self.handle_selected == self.handle_bottom_left:
            fromX = self.mouse_press_rect.left()
            fromY = self.mouse_press_rect.bottom()
            toX = fromX + mouse_pos.x() - self.mouse_press_pos.x()
            toY = fromY + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setBottom(boundingRect.bottom() - offset)
            # Prevent overlapping.
            if rect.left() >= rect.right():
                rect.setLeft(rect.right() - min_size)
            if rect.bottom() <= rect.top():
                rect.setBottom(rect.top() + min_size)

        elif self.handle_selected == self.handle_bottom_middle:
            fromY = self.mouse_press_rect.bottom()
            toY = fromY + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            # Prevent overlapping.
            if rect.bottom() <= rect.top():
                rect.setBottom(rect.top() + min_size)

        elif self.handle_selected == self.handle_bottom_right:
            fromX = self.mouse_press_rect.right()
            fromY = self.mouse_press_rect.bottom()
            toX = fromX + mouse_pos.x() - self.mouse_press_pos.x()
            toY = fromY + mouse_pos.y() - self.mouse_press_pos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            # Prevent overlapping.
            if rect.right() <= rect.left():
                rect.setRight(rect.left() + min_size)
            if rect.bottom() <= rect.top():
                rect.setBottom(rect.top() + min_size)

        # Make sure it's not possible to resize past 'max_rect' bounds.
        rect = rect.intersected(self.max_rect)
        self.setRect(rect)
        self.__update_handles_pos()

        # Emit the new dimensions of the cropper.
        top_l_x = round(self.rect().x())
        top_l_y = round(self.rect().y())
        width = round(self.rect().width())
        height = round(self.rect().height())
        self.scene.cropper_resized_signal.emit(top_l_x, top_l_y, width, height)
