# Frontend - Home Irrigation Web Client

Next.js web application for controlling and monitoring the home irrigation system.

## Features

- Real-time sensor data display (air and soil conditions)
- Manual valve control
- Auto/Manual mode switching
- Dynamic threshold configuration
- Calendar-based watering schedules
- Mobile-responsive design

## Setup

### Install Dependencies

```bash
cd client
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

### Docker Build

```bash
cd client
docker build -t irrigation-client .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://backend:8000 irrigation-client
```

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

## Mobile Access

The web interface is optimized for mobile devices. Access it from your smartphone using the Raspberry Pi's IP address:

```
http://<raspberry-pi-ip>:3000
```

