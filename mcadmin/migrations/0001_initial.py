# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ManagementCommandAdminGroup'
        db.create_table('mcadmin_managementcommandadmingroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('mcadmin', ['ManagementCommandAdminGroup'])

        # Adding model 'ManagementCommandAdminGroupPermission'
        db.create_table('mcadmin_managementcommandadmingrouppermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='permissions', to=orm['mcadmin.ManagementCommandAdminGroup'])),
            ('user_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
        ))
        db.send_create_signal('mcadmin', ['ManagementCommandAdminGroupPermission'])

        # Adding unique constraint on 'ManagementCommandAdminGroupPermission', fields ['group', 'user_group']
        db.create_unique('mcadmin_managementcommandadmingrouppermission', ['group_id', 'user_group_id'])

        # Adding model 'ManagementCommandAdminCommand'
        db.create_table('mcadmin_managementcommandadmincommand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('command', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='commands', to=orm['mcadmin.ManagementCommandAdminGroup'])),
        ))
        db.send_create_signal('mcadmin', ['ManagementCommandAdminCommand'])

        # Adding unique constraint on 'ManagementCommandAdminCommand', fields ['command', 'group']
        db.create_unique('mcadmin_managementcommandadmincommand', ['command', 'group_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ManagementCommandAdminCommand', fields ['command', 'group']
        db.delete_unique('mcadmin_managementcommandadmincommand', ['command', 'group_id'])

        # Removing unique constraint on 'ManagementCommandAdminGroupPermission', fields ['group', 'user_group']
        db.delete_unique('mcadmin_managementcommandadmingrouppermission', ['group_id', 'user_group_id'])

        # Deleting model 'ManagementCommandAdminGroup'
        db.delete_table('mcadmin_managementcommandadmingroup')

        # Deleting model 'ManagementCommandAdminGroupPermission'
        db.delete_table('mcadmin_managementcommandadmingrouppermission')

        # Deleting model 'ManagementCommandAdminCommand'
        db.delete_table('mcadmin_managementcommandadmincommand')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mcadmin.managementcommandadmincommand': {
            'Meta': {'ordering': "['command']", 'unique_together': "(['command', 'group'],)", 'object_name': 'ManagementCommandAdminCommand'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commands'", 'to': "orm['mcadmin.ManagementCommandAdminGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mcadmin.managementcommandadmingroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'ManagementCommandAdminGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'mcadmin.managementcommandadmingrouppermission': {
            'Meta': {'ordering': "['group']", 'unique_together': "(['group', 'user_group'],)", 'object_name': 'ManagementCommandAdminGroupPermission'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'to': "orm['mcadmin.ManagementCommandAdminGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"})
        }
    }

    complete_apps = ['mcadmin']
