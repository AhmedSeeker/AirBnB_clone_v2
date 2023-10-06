#Redo task 0 by using Puppet

exec {'directories':
  command  => 'mkdir -p /data/web_static/releases/test/; mkdir -p /data/web_static/shared/',
  provider => shell,
}

file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n",
}

file {'/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  require => Exec['directories'],
}

exec {'ubuntu':
  command  => 'chown -R ubuntu:ubuntu /data/',
  provider => shell,
  require  => Exec['directories'],
}

exec {'apt-get update':
  provider => shell,
  notify   => Package['nginx'],
}

package {'nginx':
  ensure   => present,
  provider => apt,
}

file_line {'hbnb_static':
  line    => "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}",
  after   => '^\troot /var/www/html;',
  path    => '/etc/nginx/sites-available/default',
  require => Package['nginx'],
  notify  => Service['nginx'],
}

service {'nginx':
  ensure => running
}
