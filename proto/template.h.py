/* template: v0.1, bindings: v${data['version']} */

% for value in data['module'].imports:
#include <proto/${value[1]}.h>
% endfor

% for (type, name) in data['simple']:
typedef ${('_').join(type.name).lower()} ${('_').join(name).lower()}_t; 
% endfor

% for (type, name) in data['enum']:
enum ${('_').join(name)} {
% for val in type.values:
    ${('_').join(name)}_${val[0]} = ${val[1]},
% endfor
}
% endfor

% for req in data['request']:
<% name = ('_').join(req.name) %>
% if req.reply:
int __impl_${name}(ClientPtr client, __req_${name} *req, __rep_${name} *rep);
% else:
int __impl_${name}(ClientPtr client, __req_${name} *req);
% endif
% endfor
