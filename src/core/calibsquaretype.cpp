/*
   * (C) 2015, Aurel Wildfellner
   *
   * This file is part of CraftUI.
   *
   * Beholder is free software: you can redistribute it and/or modify
   * it under the terms of the GNU General Public License as published by
   * the Free Software Foundation, either version 3 of the License, or
   * (at your option) any later version.
   *
   * Beholder is distributed in the hope that it will be useful,
   * but WITHOUT ANY WARRANTY; without even the implied warranty of
   * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   * GNU General Public License for more details.
   *
   * You should have received a copy of the GNU General Public License
   * along with CraftUI. If not, see <http://www.gnu.org/licenses/>. */

#include "calibsquaretype.h"


void CalibSquareType::loadFromFileStorage(const cv::FileNode& node) {
    ElementType::loadFromFileStorage(node);
    node["length"] >> length;
    node["width"] >> width;
}

void CalibSquareType::saveToFileStorage(cv::FileStorage& fs) {
    fs << elementname << "{";
    ElementType::saveToFileStorage(fs);
    fs << "length" << length;
    fs << "width" << width;
    fs << "}";
}


Element::Ptr CalibSquareType::createDefaultElement() {
    return NULL;
}

