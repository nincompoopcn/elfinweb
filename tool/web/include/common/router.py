from ..issue import IssueView
from ..metric import MetricView
from ..helper import HelperView
from ..login import LoginView
from ..logout import LogoutView
from ..group import GroupView
from ..area import AreaView
from ..fault import FaultView
from ..privilege import PrivilegeView
from ..admin import AdminView
from ..third import ProntoView, PersonView

router = {
    'issue_view': {
        'view': IssueView,
        'url': {
            '/': ['GET'],
            '/issue/': ['GET', 'POST'],
            '/issue/<int:i_id>': ['GET', 'PUT', 'DELETE']
        }
    },
    'metric_view': {
        'view': MetricView,
        'url': {
            '/metric/': ['GET'],
            '/metric/<int:m_id>': ['GET']
        }
    },
    'helper_view': {
        'view': HelperView,
        'url': {
            '/helper/': ['GET', 'POST']
        }
    },
    'login_view': {
        'view': LoginView,
        'url': {
           '/login/': ['GET', 'POST']
        }
    },
    'logout_view': {
        'view': LogoutView,
        'url': {
            '/logout/': ['GET']
        }
    },
    'group_view': {
        'view': GroupView,
        'url': {
            '/group/': ['GET'],
            '/group/<int:g_id>': ['GET', 'PUT']
        }
    },
    'area_view': {
        'view': AreaView,
        'url': {
            '/area/': ['GET']
        }
    },
    'fault_view': {
        'view': FaultView,
        'url': {
            '/fault/': ['GET', 'POST'],
            '/fault/<int:f_id>': ['GET', 'PUT', 'DELETE']
        }
    },
    'privilege_view': {
        'view': PrivilegeView,
        'url': {
            '/privilege/': ['GET', 'POST'],
            '/privilege/<u_id>': ['DELETE']
        }
    },
    'admin_view': {
        'view': AdminView,
        'url': {
            '/admin/': ['GET']
        }
    },
    'pronto_view': {
        'view': ProntoView,
        'url': {
            '/third/pronto/<p_id>': ['GET']
        }
    },
    'person_view': {
        'view': PersonView,
        'url': {
            '/third/person/': ['GET']
        }
    }
}