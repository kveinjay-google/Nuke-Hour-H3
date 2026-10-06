/* SPDX-License-Identifier: GPL-2.0-or-later */
#pragma once

#include <QObject>
#include <QEvent>
#include <QAbstractButton>
#include <QPushButton>
#include <QToolButton>
#include <QPainter>
#include <QStyleOptionButton>
#include <QStyleOptionToolButton>
#include <array>
#include <algorithm>

class FantasyButtonArt final : public QObject
{
 struct Plate
 {
  QPixmap image;
  QRect bounds;
 };
 std::array<std::array<Plate, 4>, 2> plates;
 QPixmap surface{":/artwork/hd-fantasy/navy-surface.png"};

 static QRect visibleBounds(const QImage & image)
 {
  int left = image.width(), top = image.height(), right = -1, bottom = -1;
  for(int y = 0; y < image.height(); ++y)
   for(int x = 0; x < image.width(); ++x)
    if(qAlpha(image.pixel(x, y)) >= 64)
    {
     left = std::min(left, x); right = std::max(right, x);
     top = std::min(top, y); bottom = std::max(bottom, y);
    }
  return right < left ? image.rect() : QRect(QPoint(left, top), QPoint(right, bottom));
 }

 static void drawPlate(QPainter & painter, const QRect & target, const Plate & plate, bool primary)
 {
  if(plate.image.isNull()) return;
  const QRect source = plate.bounds;
  const int sx = source.width() / (primary ? 8 : 16);
  const int sy = source.height() / 5;
  const int dx = std::min(target.width() / 4, primary ? 36 : 14);
  const int dy = std::min(target.height() / 4, primary ? 13 : 7);
  const std::array<int, 4> xs = {source.left(), source.left() + sx, source.right() + 1 - sx, source.right() + 1};
  const std::array<int, 4> ys = {source.top(), source.top() + sy, source.bottom() + 1 - sy, source.bottom() + 1};
  const std::array<int, 4> xd = {target.left(), target.left() + dx, target.right() + 1 - dx, target.right() + 1};
  const std::array<int, 4> yd = {target.top(), target.top() + dy, target.bottom() + 1 - dy, target.bottom() + 1};
  for(int y = 0; y < 3; ++y)
   for(int x = 0; x < 3; ++x)
    painter.drawPixmap(QRect(xd[x], yd[y], xd[x+1] - xd[x], yd[y+1] - yd[y]), plate.image,
     QRect(xs[x], ys[y], xs[x+1] - xs[x], ys[y+1] - ys[y]));
 }

public:
 explicit FantasyButtonArt(QWidget * parent) : QObject(parent)
 {
  const std::array<QString, 2> families = {QStringLiteral("primary"), QStringLiteral("secondary")};
  const std::array<QString, 4> states = {QStringLiteral("normal"), QStringLiteral("pressed"), QStringLiteral("active"), QStringLiteral("disabled")};
  for(size_t f = 0; f < families.size(); ++f)
   for(size_t s = 0; s < states.size(); ++s)
   {
    QImage image(QString(":/artwork/hd-fantasy/%1-%2.png").arg(families[f], states[s]));
    plates[f][s] = {QPixmap::fromImage(image), visibleBounds(image)};
   }
 }

 bool eventFilter(QObject * watched, QEvent * event) override
 {
  if(event->type() != QEvent::Paint) return false;
  auto * widget = qobject_cast<QWidget *>(watched);
  auto * scope = qobject_cast<QWidget *>(parent());
  if(!widget || !scope || (widget != scope && !scope->isAncestorOf(widget))) return false;
  if(widget && (widget->property("surface").toString() == QStringLiteral("card") || widget->objectName() == QStringLiteral("sidePanel")))
  {
   QPainter painter(widget);
   painter.fillRect(widget->rect(), QColor("#12283c"));
   painter.setOpacity(0.22);
   painter.drawTiledPixmap(widget->rect(), surface);
   return true;
  }
  auto * push = qobject_cast<QPushButton *>(watched);
  auto * tool = qobject_cast<QToolButton *>(watched);
  QAbstractButton * button = push ? static_cast<QAbstractButton *>(push) : tool;
  if(!button || button->width() <= 0 || button->height() <= 0) return false;
  const bool primary = button->property("role").toString() == QStringLiteral("primary");
  const int state = !button->isEnabled() ? 3 : button->isDown() ? 1 : button->isChecked() || button->hasFocus() || button->underMouse() ? 2 : 0;
  QPainter painter(button);
  painter.setRenderHint(QPainter::SmoothPixmapTransform);
  const bool navigation = button->parentWidget() && button->parentWidget()->objectName() == QStringLiteral("sidePanel");
  if(!navigation || state == 1 || button->isChecked() || button->hasFocus())
   drawPlate(painter, button->rect().adjusted(1, 1, -1, -1), plates[primary ? 0 : 1][state], primary);
  QPalette palette = button->palette();
  const QColor text = !button->isEnabled() ? QColor("#a6a9ab") : primary ? QColor("#291d10") : QColor("#f5e8cc");
  palette.setColor(QPalette::ButtonText, text);
  palette.setColor(QPalette::Text, text);
  if(push)
  {
   QStyleOptionButton option;
   option.initFrom(push);
   option.palette = palette;
   option.rect = button->rect().adjusted(primary ? 40 : 14, 6, primary ? -40 : -14, -6);
   if(button->isDown()) option.rect.translate(0, 2);
   option.text = push->text(); option.icon = push->icon(); option.iconSize = push->iconSize();
   if(push->isChecked()) option.state |= QStyle::State_On;
   push->style()->drawControl(QStyle::CE_PushButtonLabel, &option, &painter, push);
  }
  else
  {
   QStyleOptionToolButton option;
   option.initFrom(tool);
   option.palette = palette;
   option.rect = button->rect().adjusted(7, 6, -7, -6);
   if(button->isDown()) option.rect.translate(0, 2);
   option.text = tool->text(); option.icon = tool->icon(); option.iconSize = tool->iconSize();
   option.toolButtonStyle = tool->toolButtonStyle(); option.arrowType = tool->arrowType();
   if(tool->isChecked()) option.state |= QStyle::State_On;
   if(tool->arrowType() != Qt::NoArrow) option.features |= QStyleOptionToolButton::Arrow;
   tool->style()->drawControl(QStyle::CE_ToolButtonLabel, &option, &painter, tool);
  }
  if(button->hasFocus())
  {
   painter.setPen(QPen(QColor("#f3cf87"), 2));
   painter.drawRoundedRect(button->rect().adjusted(6, 6, -6, -6), 2, 2);
  }
  return true;
 }
};
