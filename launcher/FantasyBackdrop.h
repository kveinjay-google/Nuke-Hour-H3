/* SPDX-License-Identifier: GPL-2.0-or-later */
#pragma once

#include <algorithm>
#include <QWidget>
#include <QPainter>
#include <QPixmap>
#include <QLinearGradient>

class FantasyBackdrop final : public QWidget
{
	QPixmap landscape{":/artwork/hd-fantasy/castle-background.png"};

public:
	explicit FantasyBackdrop(QWidget * parent = nullptr) : QWidget(parent) {}

protected:
	void paintEvent(QPaintEvent *) override
	{
		QPainter painter(this);
		painter.fillRect(rect(), QColor("#102235"));
		if(!landscape.isNull() && width() > 0 && height() > 0)
		{
			const qreal scale = std::max(qreal(width()) / landscape.width(), qreal(height()) / landscape.height());
			const QSizeF sourceSize(width() / scale, height() / scale);
			const QRectF source((landscape.width() - sourceSize.width()) / 2,
				(landscape.height() - sourceSize.height()) / 2, sourceSize.width(), sourceSize.height());
			painter.drawPixmap(QRectF(rect()), landscape, source);
		}
		QLinearGradient shade(0, 0, width(), 0);
		shade.setColorAt(0, QColor(6, 20, 34, 170));
		shade.setColorAt(0.42, QColor(6, 20, 34, 75));
		shade.setColorAt(1, QColor(6, 20, 34, 0));
		painter.fillRect(rect(), shade);
	}
};
