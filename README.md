# Airport Analysis Dashboard

A modern, interactive web dashboard for analyzing airport performance data from Bengaluru (BLR) and Delhi (DEL) airports.

## Features

### 🎯 **Overview Dashboard**
- **Key Metrics**: Total flights analyzed, average delays, on-time performance, and peak hours
- **Interactive Charts**: Flight volume comparison and delay distribution analysis
- **Real-time Statistics**: Live updates and performance indicators

### 🏙️ **City-Specific Analysis**
- **Bengaluru (BLR) Tab**: 
  - Flight type distribution (Domestic vs International)
  - Top airlines by flight count
  - Hourly traffic patterns
  - Delay heatmap by time periods
  
- **Delhi (DEL) Tab**:
  - Comprehensive Delhi airport metrics
  - Carrier performance analysis
  - Traffic flow visualization
  - Delay pattern analysis

### ⚖️ **Comparison Analysis**
- **Side-by-side Metrics**: Direct comparison between airports
- **Performance Benchmarks**: On-time performance, delay patterns, carrier efficiency
- **Trend Analysis**: Daily flight volume patterns and delay severity distribution

### 🤖 **AI Assistant Chatbot**
- **Interactive Q&A**: Ask questions about airport data and performance
- **Smart Responses**: Context-aware answers about delays, volumes, airlines, and trends
- **Real-time Support**: Get instant insights about your data

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js for interactive visualizations
- **Styling**: Modern CSS with gradients, animations, and responsive design
- **Icons**: Font Awesome for beautiful UI elements

## Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No additional installations required

### Installation
1. Clone or download the project files
2. Open `index.html` in your web browser
3. The dashboard will load automatically with all interactive features

### File Structure
```
airport-analysis-dashboard/
├── index.html          # Main dashboard page
├── styles.css          # Modern styling and animations
├── script.js           # Interactive functionality and charts
├── README.md           # This documentation
├── data/               # Airport data files
│   ├── blore_airport_data.csv
│   ├── delhi_airport_data.csv
│   └── ...
└── plots/              # Static plot images (for reference)
    ├── 01_flight_volume_comparison.png
    ├── 02_bangalore_flight_type_distribution.png
    └── ...
```

## Usage Guide

### Navigation
- **Overview Tab**: Get a quick summary of all airport metrics
- **Bengaluru Tab**: Detailed analysis of Bengaluru International Airport
- **Delhi Tab**: Comprehensive Delhi airport performance data
- **Comparison Tab**: Side-by-side analysis of both airports

### Interactive Features
- **Hover Effects**: Charts respond to mouse interactions
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Smooth Animations**: Elegant transitions between tabs and sections
- **Real-time Updates**: Dynamic chart rendering and data visualization

### Chatbot Usage
1. Click the "AI Assistant" button in the bottom-right corner
2. Type your question about airport data
3. Get instant, contextual responses about:
   - Flight delays and performance
   - Traffic volumes and patterns
   - Airline comparisons
   - Peak hours and congestion
   - On-time performance metrics

## Key Insights

### Bengaluru Airport (BLR)
- **Total Flights**: 5,176
- **Average Delay**: 15.2 minutes
- **On-Time Rate**: 82.1%
- **Peak Hours**: 6-9 AM, 6-9 PM
- **Dominant Carrier**: IndiGo

### Delhi Airport (DEL)
- **Total Flights**: 8,711
- **Average Delay**: 10.8 minutes
- **On-Time Rate**: 76.3%
- **Peak Hours**: 6-9 AM, 6-9 PM
- **Dominant Carrier**: IndiGo

## Customization

### Adding New Data
1. Update the CSV files in the `data/` folder
2. Modify the chart data in `script.js`
3. Add new chart functions as needed

### Styling Changes
- Edit `styles.css` for visual modifications
- Update color schemes, fonts, or layouts
- Modify animations and transitions

### Chatbot Enhancement
- Extend the `generateBotResponse()` function in `script.js`
- Add new response patterns and keywords
- Integrate with external APIs for real-time data

## Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- **Fast Loading**: Optimized for quick page loads
- **Smooth Interactions**: 60fps animations and transitions
- **Responsive**: Adapts to all screen sizes
- **Lightweight**: Minimal external dependencies

## Future Enhancements

- [ ] Real-time data integration
- [ ] Advanced filtering options
- [ ] Export functionality for reports
- [ ] Additional airport data sources
- [ ] Machine learning insights
- [ ] Predictive analytics
- [ ] User authentication and saved preferences

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Built with ❤️ by GPS*

