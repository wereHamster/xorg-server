/* template: v0.1, bindings: v${version} */

% for value in module.imports:
#include <proto/${value[1]}.h>
% endfor

% for (type, name) in simple:
typedef ${('_').join(type.name).lower()} ${('_').join(name).lower()}_t; 
% endfor

% for (type, name) in enum:
enum ${('_').join(name)} {
% for val in type.values:
    ${('_').join(name)}_${val[0]} = ${val[1]},
% endfor
}
% endfor

% for req in request:
<% name = ('_').join(req.name[1:]) %>
struct req_${name} {
% for field in req.fields:
    ${('_').join(field.type.name)} ${field.field_name};
% endfor
};

% if req.reply:
struct rep_${name} {
% for field in req.reply.fields:
    ${('_').join(field.type.name)} ${field.field_name};
% endfor
};

int impl_${name}(ClientPtr client, __req_${name} *req, __rep_${name} *rep);
% else:
int impl_${name}(ClientPtr client, __req_${name} *req);
% endif
% endfor
