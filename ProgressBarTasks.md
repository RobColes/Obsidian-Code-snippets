```datacorejsx
// All datacore views should return a React component; in practice, this is going to be
function StatusBar({ completed, total, label = "Progress" }) {
  const percentage = total === 0 ? 100 : Math.round((completed / total) * 100);
  
  return (
    <div style={{ width: '100%', padding: '8px' }}>
      <div style={{ marginBottom: '8px' }}>
        <span style={{ float: 'left' }}>
          {label}: {completed}/{total} completed, {percentage}%
        </span>
        <div style={{ clear: 'both' }}></div>
      </div>
      <div style={{ 
        width: '100%', 
        backgroundColor: 'black', 
        borderRadius: '9999px', 
        height: '16px',
        border: '1px solid var(--color-accent)',
        overflow: 'hidden'
      }}>
        <div 
          style={{ 
            backgroundColor: 'var(--color-accent)', 
            height: '100%', 
            borderRadius: '9999px', 
            width: `${percentage}%`,
            transition: 'width 0.3s ease-out'
          }}
        />
      </div>
    </div>
  );
}

// Main View component using the StatusBar
return function View() {
  const current = dc.useCurrentFile().$file;
  const completed = dc.useQuery("@task and $completed = true and $file = \"" + current + "\"").length;
  const total = dc.useQuery("@task and $file = \"" + current + "\"").length;

  return (
    <StatusBar 
      completed={completed} 
      total={total} 
      label="Progress" 
    />
  );
}
```