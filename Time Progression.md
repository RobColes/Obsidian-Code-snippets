```datacorejsx
function ProgressBar({ value, label }) {
  return (
    <tr style={{ borderBottom: '1px solid #334155' }}>
      <td style={{ 
        padding: '8px 12px', 
        fontWeight: '600', 
        color: '#e5e7eb',
        minWidth: '130px',
        width: '20%',
        whiteSpace: 'nowrap'
      }}>
        {label}
      </td>
      <td style={{ 
        padding: '8px 12px',
        width: '55%'
      }}>
        <div style={{ 
          width: '100%', 
          backgroundColor: '#23272f', 
          borderRadius: '9999px', 
          height: '16px',
          position: 'relative',
          overflow: 'hidden',
          minWidth: '60px'
        }}>
          <div style={{ 
            background: 'linear-gradient(to right, #3b82f6, #8b5cf6)', 
            height: '16px', 
            borderRadius: '9999px', 
            transition: 'width 0.3s ease-out',
            width: value + '%'
          }} />
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(to right, transparent, rgba(255,255,255,0.08), transparent)',
            animation: 'pulse 2s infinite'
          }} />
        </div>
      </td>
      <td style={{ 
        padding: '8px 12px', 
        textAlign: 'center', 
        fontFamily: 'monospace', 
        fontSize: '16px', 
        fontWeight: '600', 
        color: '#f3f4f6',
        minWidth: '60px',
        width: '25%',
        whiteSpace: 'nowrap'
      }}>
        {value}%
      </td>
    </tr>
  );
}

// Main View component
return function View() {
  const birthday = new Date('1962-03-28');
  const lifespanYears = 86.6;
  const deathday = new Date(birthday.getFullYear() + lifespanYears, birthday.getMonth(), birthday.getDate());

  const progress = (type) => {
    let value;
    const today = new Date();

    switch(type) {
      case "lifespan":
        const totalLifeMs = deathday.getTime() - birthday.getTime();
        const livedMs = today.getTime() - birthday.getTime();
        value = (livedMs / totalLifeMs) * 100;
        break;
      
      case "year":
        const startOfYear = new Date(today.getFullYear(), 0, 1);
        const endOfYear = new Date(today.getFullYear() + 1, 0, 1);
        const yearProgress = (today.getTime() - startOfYear.getTime()) / (endOfYear.getTime() - startOfYear.getTime());
        value = yearProgress * 100;
        break;
      
      case "month":
        const daysInMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0).getDate();
        value = (today.getDate() / daysInMonth) * 100;
        break;
      
      case "day":
        value = (today.getHours() / 24) * 100;
        break;
      
      default:
        value = 0;
    }

    return Math.floor(value);
  };

  return (
    <div style={{ 
      maxWidth: '1024px', 
      margin: '0 auto', 
      padding: '16px', 
      backgroundColor: '#18181b', 
      borderRadius: '12px', 
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)',
      overflowX: 'auto'
    }}>
      <div style={{ 
        backgroundColor: '#23272f', 
        borderRadius: '8px', 
        overflow: 'hidden', 
        boxShadow: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.3)',
        minWidth: '280px'
      }}>
        <table style={{ 
          width: '100%',
          tableLayout: 'fixed',
          borderCollapse: 'collapse'
        }}>
          <thead style={{ background: 'linear-gradient(to right, #23272f, #18181b)' }}>
            <tr>
              <th style={{ 
                padding: '12px 8px', 
                textAlign: 'left', 
                fontSize: '12px', 
                fontWeight: '600', 
                color: '#cbd5e1', 
                textTransform: 'uppercase', 
                letterSpacing: '0.05em',
                width: '25%'
              }}>
                Period
              </th>
              <th style={{ 
                padding: '12px 8px', 
                textAlign: 'left', 
                fontSize: '12px', 
                fontWeight: '600', 
                color: '#cbd5e1', 
                textTransform: 'uppercase', 
                letterSpacing: '0.05em',
                width: '50%'
              }}>
                Progress
              </th>
              <th style={{ 
                padding: '12px 8px', 
                textAlign: 'center', 
                fontSize: '12px', 
                fontWeight: '600', 
                color: '#cbd5e1', 
                textTransform: 'uppercase', 
                letterSpacing: '0.05em',
                width: '25%'
              }}>
                %
              </th>
            </tr>
          </thead>
          <tbody>
            <ProgressBar value={progress("day")} label="Day" />
            <ProgressBar value={progress("month")} label="Month" />
            <ProgressBar value={progress("year")} label="Year" />
            <ProgressBar value={progress("lifespan")} label="Life" />
          </tbody>
        </table>
      </div>
    </div>
  );
}
```
