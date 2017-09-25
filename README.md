# pratica voor apt

## Changes
** hwlib/library/hwlib-native.hpp **
Remove the windows include
```
#include <Windows.h>
```
Add the chrono include
```
#include <chrono>
```

Replace the now_ticks() function with the following:
```
uint64_t now_ticks(){
    std::chrono::milliseconds ms = std::chrono::duration_cast< std::chrono::milliseconds >(std::chrono::system_clock::now().time_since_epoch());
    return ms.count();
}
```